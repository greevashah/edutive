from flask import Flask, render_template,json,request
import pymysql


# database connection
connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
cursor=connection.cursor() 


app=Flask(__name__)

# FUNCTIONS 
# Query functions
def selectquery():
    retrieve="Select * from `questiondata` "
    cursor.execute(retrieve)
 
    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows
    #     print(row)

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

def insertDataset():
    for i in range(len(qnum)):
        insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES("+str(qnum[i])+","+str(ans[i])+","+str(elapt[i])+","+str(optch[i])+",0,'"+str(totaltime)+"','"+topic[i]+"','"+difficulty[i]+"')"
        # insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        connection.commit()
        print(str(insert))

# Computation functions
def computeRows():
    # print(type(qnum))
    # print(type(rows))
    global topic,difficulty
    topic=[]
    difficulty=[]
    for q in qnum:
        difficulty.append(rows[q-1][9])     #list of string
        topic.append(rows[q-1][10])
    print(topic)
    print(difficulty)

def convertToIntList(arr):
    result=[]
    # result=[int(q) for q in arr.strip('][').split(',')]    #converted a string like "[0,1,0]" to list of integers [0,1,0] 
    for q in arr.strip('][').split(','):
        if q=='null':
            result.append(-1)
        else:
            result.append(int(q,10))
    # ques[0]=ques[0][1:]
    # ques[len(ques)-1]=ques[len(ques)-1][0:-1]
    return result

# ROUTING
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/test')
def test():
    global rows,rows1,rows2,rows3,rows4
    rows=selectquery()
    rows1=selecttopic1()
    rows2=selecttopic2()
    rows3=selecttopic3()
    rows4=selecttopic4()
    #print(type(rows))
    return render_template('test.html',value=rows,value1=rows1,value2=rows2,value3=rows3,value4=rows4)
# Sends all rows as value, possible due to render template

@app.route('/sendparameters',methods=['POST'])
def get_data():
    global qnum,ans,optch,elapt,totaltime
    qnum=convertToIntList(request.form['questions'])
    ans=convertToIntList(request.form['answers'])
    # print(type(arr1))
    optch=convertToIntList(request.form['optionchanges'])
    # print(arr2)
    elapt=convertToIntList(request.form['elapsedtime'])
    # print(arr3)
    totaltime=request.form['totalTimeTaken']
    # print(type(arr4))
    computeRows()
    insertDataset()
    return 200

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, debug=True)

#commiting the connection then closing it. Otherwise the updated change is unsaved
connection.commit()
connection.close()