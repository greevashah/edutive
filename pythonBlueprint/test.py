from flask import Flask,Blueprint, render_template
from models.query import selectquery , selectTopiclevelratio
from models.computation import randomQuestion
import calendar,time

testB=Blueprint('testB',__name__)

@testB.route('/test') #selectquery selectTopiclevelratio randomQuestion
def test():
    global rows,rows1,rows2,rows3,rows4
    global ts,testId
    ts=calendar.timegm(time.gmtime())
    testId=str(ts)
    # print("Time stamp is "+str(ts))
    # print(selectTopicTable("questiondata","TSD"))
    
    # print(randomQuestion(5,"SI","Level 2"))
    # Fetch topic-level ratio from db and then using randomQuestion() we will setch random questions acc to that ratio and then pass only
    # those selected questions
    rows=selectquery("questiondata")
    # rows1=selectTopicTable("questiondata","TSD")
    # rows2=selectTopicTable("questiondata","TW")
    # rows3=selectTopicTable("questiondata","SI")
    # rows4=selectTopicTable("questiondata","PPL")
    questionNumbers=[]
    quesRows=[]
    value=selectTopiclevelratio()
    # print(value)
    for i in range(4):
        for l in range(3):
            result= randomQuestion(value[i][l+2], value[i][1],"Level "+str(l+1))
            questionNumbers += result[0]
            quesRows += result[1]
    # print(questionNumbers)
    # print(len(questionNumbers))
    # print(tuple(quesRows))
    return render_template('test.html',value=tuple(quesRows), value1=questionNumbers)
    # print(type(rows))
    # return render_template('test.html',value=rows,value1=rows1,value2=rows2,value3=rows3,value4=rows4)
# Sends all rows as value, possible due to render template
