from flask import Flask, render_template,json,request
import pymysql


# database connection
connection= pymysql.connect(host="eu-cdbr-west-03.cleardb.net",user="b72668611cc1ee",passwd="822351e1",database="heroku_279e13e2a650fcd")
# connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
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
        insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES("+str(qnum[i])+","+str(ans[i])+","+str(elapt[i])+","+str(optch[i])+","+str(timept[topic[i]])+",'"+str(totaltime)+"','"+topic[i]+"','"+difficulty[i]+"')"
        # insert="INSERT INTO `dataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert)
        connection.commit()
        # print(str(insert))

def insertTopicDataset():
    for i in topicwise.keys():
        insert="INSERT INTO `topicdataset`(topic, correctness, tpque, optionchanges, tptopic, tptest) VALUES('"+i+"','"+str(topicwise[i][0])+"','"+str(topicwise[i][1])+"','"+str(topicwise[i][2])+"','"+str(timept[i])+"','"+str(totaltime)+"')"
        # insert="INSERT INTO `topicdataset`(qno, correctness, tpque, optionchanges, tptopic, tptest, topic, difficulty) VALUES(%d,%d,%d,%d,%d,%s,%s,%s)"
        cursor.execute(insert) 
        connection.commit()
        print(str(insert))

# Computation functions
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
    print(topic)
    print(difficulty)
    print(topicQ)
    print(timept)

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
    print(topicwise)

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
    print("Here in result")
    ds= selectquery("dataset")
    topicds=selectquery("topicdataset")
    return render_template('result.html', value=str(ds), value1=str(topicds) )

@app.route('/test')
def test():
    global rows,rows1,rows2,rows3,rows4
    rows=selectquery("questiondata")
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
    computeTopicwise()
    insertTopicDataset()
    print("Leaving sendparameters")
    return "lol"

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, debug=True)

#commiting the connection then closing it. Otherwise the updated change is unsaved
connection.commit()
connection.close()