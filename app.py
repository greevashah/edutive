from flask import Flask, render_template,json
import pymysql


# database connection
connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
cursor=connection.cursor() 


def selectquery():
    retrieve="Select * from `questiondata` "
    cursor.execute(retrieve)
 
    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows
    #     print(row)
"""
def selectlevel1():
    get1="Select * from `questiondata` where `Difficulty`='Level 1' "
    cursor.execute(get1)
    rows1= cursor.fetchall()
    return rows1

def selectlevel2():
    get2="Select * from `questiondata` where `Difficulty`='Level 2' "
    cursor.execute(get2)
    rows2= cursor.fetchall()
    return rows2

def selectlevel3():
    get3="Select * from `questiondata` where `Difficulty`= 'Level 3' "
    cursor.execute(get3)
    rows3= cursor.fetchall()
    return rows3
"""

def selecttopic1():
    get1="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='TSD' "
    cursor.execute(get1)
    rows1= cursor.fetchall()
    return rows1

def selecttopic2():
    get2="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='TW'"
    cursor.execute(get2)
    rows2= cursor.fetchall()
    return rows2

def selecttopic3():
    get3="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='SI' "
    cursor.execute(get3)
    rows3= cursor.fetchall()
    return rows3

def selecttopic4():
    get3="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='PPL'"
    cursor.execute(get3)
    rows4= cursor.fetchall()
    return rows4

# queries
# retrieve="Select * from `questiondata` where `question no`=3;"
# selectquery()

# insert="Insert into student values('abc','1234','abc@gmail.com')"
# cursor.execute(insert)
# print("After INSERT")
# selectquery()


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/test')
def test():
    rows=selectquery()
    rows1=selecttopic1()
    rows2=selecttopic2()
    rows3=selecttopic3()
    rows4=selecttopic4()
    #print(type(rows))
    return render_template('test.html',value=rows,value1=rows1,value2=rows2,value3=rows3,value4=rows4)
# Sends all rows as value, possible due to render template

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, debug=True)

#commiting the connection then closing it. Otherwise the updated change is unsaved
connection.commit()
connection.close()