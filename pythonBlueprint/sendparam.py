from flask import Flask,Blueprint, render_template, request
# from models.query import insertTopicDataset , insertDataset , insertTestDataset
# from models.computation import convertToIntList , computeRows, computeTopicwise
import pymysql

send=Blueprint('send',__name__)

# TestID
@send.route('/sendparameters',methods=['POST']) #convertToIntList computeRows() insertDataset() computeTopicwise() insertTopicDataset() insertTestDataset()
def get_data():
    global qnum,ans,optch,elapt,totaltime,totalcorrect,totalincorrect,testscore,testId,rows

    rows=selectquery("questiondata")

    qnum=convertToIntList(request.form['questions'])
    ans=convertToIntList(request.form['answers'])
    # print(type(arr1))
    optch=convertToIntList(request.form['optionchanges'])
    # print(arr2)
    elapt=convertToIntList(request.form['elapsedtime'])
    # print(arr3)
    totaltime=request.form['totalTimeTaken']
    # print(type(arr4))
    totalcorrect=request.form['totalcorrect']
    totalincorrect=request.form['totalincorrect']
    testscore=request.form['testscore']
    testId=request.form['testId']
    
    print("Reached here")
    print(elapt)
    computeRows()
    insertDataset()
    computeTopicwise()
    insertTopicDataset()
    insertTestDataset()

    print("Leaving sendparameters")
    return "lol"

def initialise_thanking():
    return ans, elapt, optch, topic, difficulty,l1,l2,l3,l4
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

def insertDataset():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    for i in range(len(qnum)):
        insert="INSERT INTO `dataset`(testId,qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES('"+testId+"',"+str(qnum[i])+","+str(ans[i])+","+str(elapt[i])+","+str(optch[i])+","+str(timept[topic[i]])+",'"+str(totaltime)+"','"+topic[i]+"','"+difficulty[i]+"')"
        # insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        connection.commit()
        # print(str(insert))

def insertTopicDataset():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    for i in topicwise.keys():
        insert="INSERT INTO `topicdataset`(testId,topic, correctness, tpque, optionchanges, tptopic,correct, incorrect, topicscore, tptest) VALUES('"+testId+"','"+i+"','"+str(topicwise[i][0])+"','"+str(topicwise[i][1])+"','"+str(topicwise[i][2])+"','"+str(timept[i])+"','"+str(topicCorrect[i])+"','"+str(topicIncorrect[i])+"','"+str(topicScore[i])+"','"+str(totaltime)+"')"
        # insert="INSERT INTO `topicdataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        # print(cursor.execute(insert))
        connection.commit()
        # print(str(insert))

def insertTestDataset():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    insert="INSERT INTO `testdataset`(`testId`, `tptest`, `totalcorrect`, `totalincorrect` , `testscore`) VALUES ('"+testId+"','"+str(totaltime)+"',"+str(totalcorrect)+","+str(totalincorrect)+","+str(testscore)+")"
    cursor.execute(insert)
    connection.commit()

# Computation
# Computing topicQ and timept dictionaries
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
    global topicwise,topicIncorrect,topicCorrect,topicScore,l1,l2,l3,l4
    topicwise=dict()
    topicCorrect=dict()
    topicIncorrect=dict()
    topicScore= dict()

    topicCorrect['TSD']=0
    topicCorrect['TW']=0
    topicCorrect['SI']=0
    topicCorrect['PPL']=0

    topicIncorrect['TSD']=0
    topicIncorrect['TW']=0
    topicIncorrect['SI']=0
    topicIncorrect['PPL']=0
    
    topicScore['TSD']=0
    topicScore['TW']=0
    topicScore['SI']=0
    topicScore['PPL']=0

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
                if(ans[c]>0):
                    topicCorrect['TSD'] +=1
                    topicScore['TSD'] +=3
                else:
                    topicIncorrect['TSD'] +=1
                    topicScore['TSD'] -=1
                topicwise['TSD'][0] += ans[c]/l1
                qattempt[0]+=1
            else:
                topicwise['TSD'][0] += 0
            topicwise['TSD'][1] += elapt[c]/l1
            topicwise['TSD'][2] += optch[c]

        elif(tmp =='TW'):
            if(ans[c] != -1):
                if(ans[c]>0):
                    topicCorrect['TW'] +=1
                    topicScore['TW'] +=3
                else:
                    topicIncorrect['TW'] +=1
                    topicScore['TW'] -=1
                topicwise['TW'][0] += ans[c]/l2
                qattempt[1]+=1
            else:
                topicwise['TW'][0] += 0
            topicwise['TW'][1] += elapt[c]/l2
            topicwise['TW'][2] += optch[c]

        elif(tmp=='SI'):
            if(ans[c] != -1):
                if(ans[c]>0):
                    topicCorrect['SI'] +=1
                    topicScore['SI'] +=3
                else:
                    topicIncorrect['SI'] +=1
                    topicScore['SI'] -=1
                topicwise['SI'][0] += ans[c]/l3
                qattempt[2]+=1
            else:
                topicwise['SI'][0] += 0
            topicwise['SI'][1] += elapt[c]/l3
            topicwise['SI'][2] += optch[c]

        elif(tmp=='PPL'):
            if(ans[c] != -1):
                if(ans[c]>0):
                    topicCorrect['PPL'] +=1
                    topicScore['PPL'] +=3
                else:
                    topicIncorrect['PPL'] +=1
                    topicScore['PPL'] -=1
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
    # print("Topicwise")
    # print(topicCorrect)
    # print(topicIncorrect)
    # print(topicScore)

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
