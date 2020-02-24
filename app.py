from flask import Flask, render_template,json,request
import pymysql,os,random,calendar,time
from decimal import *

# database connection
# connection= pymysql.connect(host="sql12.freemysqlhosting.net",user="sql12322245",passwd="PfmNYfbQGj",database="sql12322245")
connection= pymysql.connect(host="remotemysql.com",user="tthTEMzAku",passwd="VDy1GLuLuT",database="tthTEMzAku")
cursor=connection.cursor() 


app=Flask(__name__)

# FUNCTIONS 
# Query functions
def selectquery(tablename):
    retrieve="Select * from `"+tablename+"` "
    cursor.execute(retrieve)
    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows
    # print(row)

#One condition
def selectWhereTable(tableName, columnname, columnvalue):       
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicLevelTable(tableName, topicName, level):
    get1="SELECT * FROM `"+tableName+"` WHERE `Difficulty` = '"+level+"' AND `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicTable(tableName, topicName):
    get1="SELECT * FROM `"+tableName+"` WHERE `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

# def selecttopic1():
#     get1="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='TSD' "
#     cursor.execute(get1)
#     rows1= cursor.fetchall()
#     return rows1

def insertDataset():
    for i in range(len(qnum)):
        insert="INSERT INTO `dataset`(testId,qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES('"+testId+"',"+str(qnum[i])+","+str(ans[i])+","+str(elapt[i])+","+str(optch[i])+","+str(timept[topic[i]])+",'"+str(totaltime)+"','"+topic[i]+"','"+difficulty[i]+"')"
        # insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        connection.commit()
        # print(str(insert))

def insertTopicDataset():
    for i in topicwise.keys():
        insert="INSERT INTO `topicdataset`(testId,topic, correctness, tpque, optionchanges, tptopic, tptest) VALUES('"+testId+"','"+i+"','"+str(topicwise[i][0])+"','"+str(topicwise[i][1])+"','"+str(topicwise[i][2])+"','"+str(timept[i])+"','"+str(totaltime)+"')"
        # insert="INSERT INTO `topicdataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        # print(cursor.execute(insert))
        connection.commit()
        # print(str(insert))

# COMPUTATION FUNCTIONS
def computeRows():
    # print(type(qnum))
    # print(type(rows))
    global topic,difficulty, timept, topicQ
    topic=[]
    difficulty=[]
    timept=dict()        #dictionary of time per topic; (Topic name)=>(Time) {TW:0,TSD:0,SI:0,PPL:0}
    timept['TSD']= 0
    timept['TW']= 0
    timept['SI']= 0
    timept['PPL']= 0
    topicQ=dict()       #dictionary which stores list of question numbers of a particular topic,[5,30,46,100] {TW:[],TSD:[],SI:[],PPL:[]}
    topicQ['TSD']=[]
    topicQ['TW']=[]
    topicQ['SI']=[]
    topicQ['PPL']=[]
    c=0
    for q in qnum:
        difficulty.append(rows[q-1][9])     #list of string
        tmp=rows[q-1][10]
        topic.append(tmp)
        if(tmp =='TW'):
            topicQ['TW'].append(q)
            timept['TW'] +=elapt[c]
        elif(tmp=='TSD'):
            topicQ['TSD'].append(q)
            timept['TSD'] += elapt[c]
        elif(tmp=='SI'):
            topicQ['SI'].append(q)
            timept['SI'] += elapt[c]
        elif(tmp=='PPL'):
            topicQ['PPL'].append(q)
            timept['PPL'] += elapt[c]
        c= c+1
    # print(topic)
    # print(difficulty)
    # print(topicQ)
    # print(timept)

def computeTopicwise():
    global topicwise
    topicwise=dict()
    topicwise['TSD']=[0]*3
    topicwise['TW']=[0]*3
    topicwise['SI']=[0]*3
    topicwise['PPL']=[0]*3

    l1= len(topicQ['TSD'])
    l2= len(topicQ['TW'])
    l3= len(topicQ['SI'])
    l4= len(topicQ['PPL'])

    c=0
    qattempt=[0]*4
    for q in qnum:
        tmp=rows[q-1][10]
        if(tmp=='TSD'):
            if(ans[c] != -1):
                topicwise['TSD'][0] += ans[c]/l1
                qattempt[0]+=1
            else:
                topicwise['TSD'][0] += 0
            topicwise['TSD'][1] += elapt[c]/l1
            topicwise['TSD'][2] += optch[c]

        elif(tmp =='TW'):
            if(ans[c] != -1):
                topicwise['TW'][0] += ans[c]/l2
                qattempt[1]+=1
            else:
                topicwise['TW'][0] += 0
            topicwise['TW'][1] += elapt[c]/l2
            topicwise['TW'][2] += optch[c]

        elif(tmp=='SI'):
            if(ans[c] != -1):
                topicwise['SI'][0] += ans[c]/l3
                qattempt[2]+=1
            else:
                topicwise['SI'][0] += 0
            topicwise['SI'][1] += elapt[c]/l3
            topicwise['SI'][2] += optch[c]

        elif(tmp=='PPL'):
            if(ans[c] != -1):
                topicwise['PPL'][0] += ans[c]/l4
                qattempt[3]+=1
            else:
                topicwise['PPL'][0] += 0
            topicwise['PPL'][1] += elapt[c]/l4
            topicwise['PPL'][2] += optch[c]
        c=c+1
    topicwise['TSD'][2] /= qattempt[0] if qattempt[0] > 0 else 1
    topicwise['TW'][2] /= qattempt[1] if qattempt[1] > 0 else 1
    topicwise['SI'][2] /= qattempt[2] if qattempt[2] > 0 else 1
    topicwise['PPL'][2] /= qattempt[3] if qattempt[3] > 0 else 1
    # print(topicwise)

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

def randomQuestion(num,topicName,level):
    allques=selectTopicLevelTable("questiondata",topicName,level)
    l= len(allques)
    questions=[]
    for i in range(num):
        temp= random.choice(allques)
        if(temp[0] not in questions):
            questions.append(temp[0])
            i+=1
    # print(questions)
    return questions

# ROUTING
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/thanking')
def thanking():
    return render_template('thanking.html')
    
@app.route('/result')
def result():
    print("Here in result")
    ds= selectWhereTable("dataset","testId",testId)
    topicds=selectWhereTable("topicdataset","testId",testId)
    newRow=[]
    for i in topicds:
        temp=[]
        for j in i:
            if type(j)==type(Decimal('0.001')):
                temp.append(float(j))
            else:
                temp.append(j)
        newRow.append(temp)
    print(newRow)
    print(type(newRow[0][3]),newRow[0][3] )
    return render_template('result.html', value=ds, value1=newRow, value2= testId)

@app.route('/test')
def test():
    global rows,rows1,rows2,rows3,rows4
    global ts,testId
    ts=calendar.timegm(time.gmtime())
    testId=str(ts)
    # print("Time stamp is "+str(ts))
    # print(selectTopicTable("questiondata","TSD"))
    # print(randomQuestion(5,"SI","Level 2"))
    rows=selectquery("questiondata")
    rows1=selectTopicTable("questiondata","TSD")
    rows2=selectTopicTable("questiondata","TW")
    rows3=selectTopicTable("questiondata","SI")
    rows4=selectTopicTable("questiondata","PPL")
    # print(type(rows))
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
    computeTopicwise()
    insertTopicDataset()
    print("Leaving sendparameters")
    return "lol"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

#commiting the connection then closing it. Otherwise the updated change is unsaved
connection.commit()
connection.close()