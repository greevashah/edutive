from flask import Flask,Blueprint, render_template, request, redirect, url_for, session
import pymysql
import re
from flask_bcrypt import Bcrypt

user=Blueprint('user',__name__)
bcrypt = Bcrypt()


@user.route('/login', methods=['GET','POST'])
def login():
# Output message if something goes wrong...
    global uname
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account= selectWhereTable1('user','Username', username)
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            if bcrypt.check_password_hash(account[2], password):
                print("Logged IN!!!")
                session['loggedin'] = True
                session['name']= account[0]
                session['username'] = account[3]
                uname= session['username']
                values= selectWhereTable1('testdataset', 'Username', uname)
                if values is None:
                    # New Joinee
                    return redirect(url_for('user.beginner'))
                else:
                    return redirect(url_for('profileB.profile'))
                # Redirect to home page
            else:
                print("Password didnt match")
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    print("Message is "+msg)
        # Get-> langing login active
    return render_template('landing.html', msg='')

# Query
#Two condition
def selectWhereTable1(tableName, columnname1, columnvalue1):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get="SELECT * FROM `"+tableName+"` WHERE `"+columnname1+"` = '"+columnvalue1+"'"
    cursor.execute(get)
    account= cursor.fetchone()
    return account

def selectWhereTable2(tableName, columnname1, columnvalue1,columnname2, columnvalue2):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get="SELECT * FROM `"+tableName+"` WHERE `"+columnname1+"` = `"+columnvalue1+"` AND `"+columnname2+"` = `"+columnvalue2+"`"
    print(get)
    cursor.execute(get)
    account= cursor.fetchone()
    return account


@user.route('/register', methods=['POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'name' in request.form and 'password2' in request.form:
        # Create variables for easy access
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']

        account= selectWhereTable('user', 'Username', username)
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
            # Validation
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email or not name:
            msg = 'Please fill out the form!'
        elif password != password2:
            msg="Passwords are not matching"
        else:
            password_hash = bcrypt.generate_password_hash(password).decode('UTF-8')
            # pwd= str(password_hash)[2:-1] 
            print("password_hash ", password_hash)
            print(type(password_hash))
            insertUserTable(name,email,password_hash,username)
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    print("Message is "+msg)
    return render_template('landing.html', msg=msg)

#One condition
def selectWhereTable(tableName, columnname, columnvalue):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

# Insert
# INSERT INTO `user`(`Name`, `Email`, `Password`, `Username`) VALUES ([value-1],[value-2],[value-3],[value-4])
def insertUserTable(name,email,password,username):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    # insert="('"+testId+"','"+str(totaltime)+"',"+str(totalcorrect)+","+str(totalincorrect)+","+str(testscore)+")"
    insert="INSERT INTO `user`(`Name`, `Email`, `Password`, `Username`) VALUES ('"+name+"','"+email+"','"+password+"','"+username+"')"
    cursor.execute(insert)
    connection.commit()

@user.route('/logout') 
def logout():
    if 'username' in session:
        session.pop('username',None)
        session.pop('name', None)
        session['loggedIn']=False
        print(session['loggedIn'])
        print("LOGGED OUT!")
        return redirect('/')

@user.route('/beginner', methods=['GET','POST'])
def beginner():
    # username= session['username']
    insertTopiclevelratio()
    return render_template('new-joinee.html', name=uname)

def insertTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    topicLevelRt={"TSD": [2,2,1], "TW":[2,1,1], "SI":[2,1,0], "PPl":[2,1,0]}
    for k in topicLevelRt.keys():
        insert="INSERT INTO `topiclevelratio`(`Topic`, `Level 1`, `Level 2`, `Level 3`,`Username`) VALUES ('"+k+"',"+str(topicLevelRt[k][0])+","+str(topicLevelRt[k][1])+","+str(topicLevelRt[k][2])+", '"+uname+"')"
        cursor.execute(insert)
        connection.commit()
