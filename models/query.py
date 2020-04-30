import pymysql



def connectionF(): 
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    return connection
  
# FUNCTIONS 
# Query functions
def selectquery(tablename):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    retrieve="Select * from `"+tablename+"` "
    cursor.execute(retrieve)
    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows

#One condition
def selectWhereTable(tableName, columnname, columnvalue):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' "
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

def selectTestScore():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    get1="SELECT * FROM `testdataset` ORDER BY `testId` desc limit 6"
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

def selectTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
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

def insertPerformance():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    insert="INSERT INTO `performance`(`testId`, `TSD`, `TW`, `SI`, `PPL`) VALUES ('"+testId+"',"+str(pq['TSD'])+","+str(pq['TW'])+","+str(pq['SI'])+","+str(pq['PPL'])+")"
    cursor.execute(insert)
    connection.commit()

def insertTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    for k in topicLevelRt.keys():
        insert="INSERT INTO `topiclevelratio`(`Topic`, `Level 1`, `Level 2`, `Level 3`) VALUES ('"+k+"',"+str(topicLevelRt[k][0])+","+str(topicLevelRt[k][1])+","+str(topicLevelRt[k][2])+")"
        cursor.execute(insert)
        connection.commit()
