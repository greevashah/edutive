from flask import Flask,Blueprint, render_template ,  session
# from models.query import selectquery , selectTopiclevelratio
# from models.computation import randomQuestion
import pymysql
import calendar,time
import random

testB=Blueprint('testB',__name__)

# Getting Rows, TestID
@testB.route('/test') #selectquery selectTopiclevelratio randomQuestion
def test():
    global rows
    global ts,testId,username
    username= session['username']
    ts=calendar.timegm(time.gmtime())
    testId=str(ts)
    # print("Time stamp is "+str(ts))
    # print(selectTopicTable("questiondata","TSD"))
    
    # print(randomQuestion(5,"SI","Level 2"))
    # Fetch topic-level ratio from db and then using randomQuestion() we will setch random questions acc to that ratio and then pass only
    # those selected questions
    rows=selectquery("questiondata")
    questionNumbers=[]
    quesRows=[]
    value=selectTopiclevelratio()
    print("stating with value " ,value)
    for i in range(4):
        for l in range(3):
            result= randomQuestion(value[i][l+2], value[i][1],"Level "+str(l+1))
            questionNumbers += result[0]
            quesRows += result[1]
    # print(questionNumbers)
    # print(len(questionNumbers))
    # print(tuple(quesRows))
    return render_template('test.html',value=tuple(quesRows), value1=questionNumbers, value2= testId)
    # print(type(rows))
    # return render_template('test.html',value=rows,value1=rows1,value2=rows2,value3=rows3,value4=rows4)
# Sends all rows as value, possible due to render template

# Query
def selectquery(tablename):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    retrieve="Select * from `"+tablename+"` "
    cursor.execute(retrieve)
    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows

def selectTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    get1="SELECT * FROM `topiclevelratio` WHERE `Username`='"+username+"' ORDER BY `id` desc limit 4"
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicLevelTable(tableName, topicName, level):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    # print(topicName)
    # print(level)
    get1="SELECT * FROM `"+tableName+"` WHERE `Difficulty` = '"+level+"' AND `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicTable(tableName, topicName):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    get1="SELECT * FROM `"+tableName+"` WHERE `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

# Compute
def randomQuestion(num, topicName, level):
    allques=selectTopicLevelTable("questiondata",topicName,level)
    # print("All questions are ", allques)
    l= len(allques)
    questions=[]
    questionsRow=[]
    if l == 0:      #when there aren't any questions of a particular type
        lev=int(level[5:])
        alt=selectTopicLevelTable("questiondata",topicName,"Level "+str(lev-1))
        # print("level is ",str(lev))
        if(len(alt)==0):
            alt=selectTopicLevelTable("questiondata",topicName,"Level "+str(lev-2))
        allques=alt
    i=0
    while(i<num):
        temp= random.choice(allques)
        if(temp[0] not in questions):
            questions.append(temp[0])
            # print("type of temp is ",type(temp))
            questionsRow.append(temp)
            i+=1
            
    # print(questions)
    result=[]
    result.append(questions)
    result.append(questionsRow)
    return result
