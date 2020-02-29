from flask import Flask, render_template,json,request
import pymysql,os,random,calendar,time
import numpy as np
from linreg import linearreg
from decimal import *

# database connection
# connection= pymysql.connect(host="sql12.freemysqlhosting.net",user="sql12322245",passwd="PfmNYfbQGj",database="sql12322245")
connection= pymysql.connect(host="remotemysql.com",user="tthTEMzAku",passwd="VDy1GLuLuT",database="tthTEMzAku",connect_timeout=6000)
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

#One condition
def selectWhereTable(tableName, columnname, columnvalue):       
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicLevelTable(tableName, topicName, level):
    # print(topicName)
    # print(level)
    get1="SELECT * FROM `"+tableName+"` WHERE `Difficulty` = '"+level+"' AND `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopicTable(tableName, topicName):
    get1="SELECT * FROM `"+tableName+"` WHERE `Topic` ='"+topicName+"' "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTestScore():
    get1="SELECT * FROM `testdataset` ORDER BY `testId` desc limit 6"
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopiclevelratio():
    get1="SELECT * FROM `topiclevelratio` ORDER BY `id` desc limit 4"
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
        insert="INSERT INTO `topicdataset`(testId,topic, correctness, tpque, optionchanges, tptopic,correct, incorrect, topicscore, tptest) VALUES('"+testId+"','"+i+"','"+str(topicwise[i][0])+"','"+str(topicwise[i][1])+"','"+str(topicwise[i][2])+"','"+str(timept[i])+"','"+str(topicCorrect[i])+"','"+str(topicIncorrect[i])+"','"+str(topicScore[i])+"','"+str(totaltime)+"')"
        # insert="INSERT INTO `topicdataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        # print(cursor.execute(insert))
        connection.commit()
        # print(str(insert))

def insertTestDataset():
    insert="INSERT INTO `testdataset`(`testId`, `tptest`, `totalcorrect`, `totalincorrect` , `testscore`) VALUES ('"+testId+"','"+str(totaltime)+"',"+str(totalcorrect)+","+str(totalincorrect)+","+str(testscore)+")"
    cursor.execute(insert)
    connection.commit()

def insertPerformance():
    insert="INSERT INTO `performance`(`testId`, `TSD`, `TW`, `SI`, `PPL`) VALUES ('"+testId+"',"+str(pq['TSD'])+","+str(pq['TW'])+","+str(pq['SI'])+","+str(pq['PPL'])+")"
    cursor.execute(insert)
    connection.commit()

def insertTopiclevelratio():
    for k in topicLevelRt.keys():
        insert="INSERT INTO `topiclevelratio`(`Topic`, `Level 1`, `Level 2`, `Level 3`) VALUES ('"+k+"',"+str(topicLevelRt[k][0])+","+str(topicLevelRt[k][1])+","+str(topicLevelRt[k][2])+")"
        cursor.execute(insert)
        connection.commit()

# COMPUTATION FUNCTIONS

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

def findRatioLevel(a,b,c,totalq):
  lt=[]
  den=a+b+c
  if den==0:
    return [0,0,0]
  lt.append(a/den*totalq)
  lt.append(b/den*totalq)
  lt.append(c/den*totalq)
  return lt

def findRatioTopic(a,b,c,d,totalq):
  lt=[]
  den=((b*c*d)+(a*c*d)+(a*b*c)+(a*b*d))/(a*b*c*d)
  if den==0:
    return [0,0,0,0]
  lt.append((1/(a*den))*totalq)
  lt.append((1/(b*den))*totalq)
  lt.append((1/(c*den))*totalq)
  lt.append((1/(d*den))*totalq)
#   den=a+b+c+d
#   lt.append(a/den*totalq)
  return lt

def findIntRatio(lt, totalq):
  lt_int=[] 
  lt_ftp=dict()
  result=dict()
  sum_int=0
  for i in range(len(lt)):
    lt_int.append(int(lt[i]))
    result[i]=lt_int[i]
    lt_ftp[i]=lt[i] - lt_int[i]
  sum_int=sum(lt_int)
  while(sum_int < totalq):
    all=lt_ftp.values()
    k= getkey(lt_ftp, max(all))
    result[k] +=1
    lt_ftp.pop(k)
    sum_int+=1
  return result

def inferenceEngine(p, totalq):
  levelRt=dict()
  # Ratio of levels for a particular topic
  if p<=0.09 :
    a=15
    b=0
    c=0
  elif(p<=0.19):
    a=13
    b=2
    c=0
  elif(p<=0.29):
    a=10
    b=5
    c=0
  elif(p<=0.39):
    a=7
    b=7
    c=1
  elif(p<=0.49):
    a=5
    b=8
    c=2
  elif(p<=0.59):
    a=3
    b=10
    c=2
  elif(p<=0.69):
    a=2
    b=8
    c=5
  elif(p<=0.79):
    a=2
    b=5
    c=8
  elif(p<=0.89):
    a=1
    b=3
    c=11
  elif(p<=1):
    a=0
    b=0
    c=15
  else:
    a=1
    b=1
    c=1
  tmp=findRatioLevel(a,b,c,totalq)
  levelRt=findIntRatio(tmp, totalq)
  # levelRt[0]=tmp[0]
  # levelRt[1]=tmp[1]
  # levelRt[2]=tmp[2]
  return(levelRt)

def getkey(lt_ftp, val):
   for key, value in lt_ftp.items(): 
     if val == value: 
       return key 

def topicRatio(pt1,pt2,pt3,pt4,totalq):
  # a:b:c:d -> 0.5:0.75:0.3:0.1
  # den= a+b+c+d
  # a/den*15:b/den*15 ...
  topicRt= dict()
  tmp=findRatioTopic(pt1,pt2,pt3,pt4,totalq)
  topicRt= findIntRatio(tmp,totalq)
  return topicRt


# ROUTING
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/thanking')
def thanking():
    global pq,topicLevelRt
    questiondataset=dict()
    for i in range(15):
        questiondataset[i]=[]
        questiondataset[i].append(ans[i])
        questiondataset[i].append(elapt[i])
        questiondataset[i].append(optch[i])
        questiondataset[i].append(topic[i])
        questiondataset[i].append(difficulty[i])
        
    timeclass=[0]*15
    optionclass=[0]*15
    count=0
    for i in questiondataset:
        if questiondataset[i][4]=="Level 1":
            if questiondataset[i][1]>40:
                timeclass[count]=3
            elif(20<questiondataset[i][1]<=40):
                timeclass[count]=2
            elif(questiondataset[i][1]<=20):
                timeclass[count]=1
        elif(questiondataset[i][4]=="Level 2"):
            if questiondataset[i][1]>80:
                timeclass[count]=3
            elif(40<questiondataset[i][1]<=80):
                timeclass[count]=2
            elif(questiondataset[i][1]<=40):
                timeclass[count]=1
        else:
            if questiondataset[i][1]>210:
                timeclass[count]=3
            elif(120<questiondataset[i][1]<=210):
                timeclass[count]=2
            elif(questiondataset[i][1]<=120):
                timeclass[count]=1
        
        if questiondataset[i][2]>=2:
            optionclass[count]=2
        elif(questiondataset[i][2]==1):
            optionclass[count]=1
        elif(questiondataset[i][2]==0):
            optionclass[count]=0
        count +=1
    x = np.array((ans,optionclass,timeclass)).T
    y=linearreg(x)
    # print(y)
    pq=dict()
    pq['TSD']=0.0
    pq['TW']=0.0
    pq['SI']=0.0
    pq['PPL']=0.0
    # y-> 15 p
    for i in range(15):
        pq[topic[i]] += y[i]
    pq['TSD'] /=l1
    pq['TW'] /=l2
    pq['SI'] /=l3
    pq['PPL'] /=l4
    # print("PQ is ", pq)
    insertPerformance()
    topicP= dict()
    topicLevelRt=dict()
    # print("No of questions per topic")
    topicRt= topicRatio(pq['TSD'],pq['TW'],pq['SI'],pq['PPL'],15)
    # print(topicRt)
    topicname=['TSD','TW','SI','PPL']
    for i in range(4):
        topicLevelRt[topicname[i]]=inferenceEngine(pq[topicname[i]], topicRt[i])

    print("No of ques of each Level in each topic")
    print(topicLevelRt) 
    insertTopiclevelratio()
    return render_template('thanking.html')


@app.route('/dashboard')
def dashboard():
    ds= selectWhereTable("dataset","testId",testId)
    topicds=selectWhereTable("topicdataset","testId",testId)
    # testds=selectWhereTable("testdataset","testId",testId)
    testds=selectTestScore()
    newRow=[]
    for i in topicds:
        temp=[]
        for j in i:
            if type(j)==type(Decimal('0.001')):
                temp.append(float(j))
            else:
                temp.append(j)
        newRow.append(temp)
    return render_template('dashboard.html', value=ds, value1=newRow, value2=testds, value3= testId)
    
@app.route('/result')
def result():
    # print("Here in result")
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
    # print(newRow)
    # print(type(newRow[0][3]),newRow[0][3] )
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

@app.route('/sendparameters',methods=['POST'])
def get_data():
    global qnum,ans,optch,elapt,totaltime,totalcorrect,totalincorrect,testscore
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
    computeRows()
    insertDataset()
    computeTopicwise()
    insertTopicDataset()
    insertTestDataset()
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