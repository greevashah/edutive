from flask import Flask,Blueprint, render_template, request , session, redirect, url_for
# from models.query import insertTopiclevelratio, insertPerformance
# from models.computation import topicRatio , inferenceEngine
import numpy as np
from linreg import linearreg
import pymysql
from pythonBlueprint.sendparam import initialise_thanking
from pythonBlueprint.profile import initialise_thankingP
# ans,elapt,optch, topic,difficulty

thankingB=Blueprint('thankingB',__name__)

# TestID
@thankingB.route('/thanking/<testId>') # insertPerformance() topicRatio inferenceEngine insertTopiclevelratio()
def thanking(testId):
    global pq,topicLevelRt,questiondataset ,username, values, testP
    ans, elapt, optch, topic, difficulty, l11,l22,l33,l44 = initialise_thanking()
    values, testP = initialise_thankingP()
    username= session['username']
    pq=dict()
    questiondataset=dict()
    topicLevelRt=dict()
    l1 = 1 if l11==0 else l11 
    l2 = 1 if l22==0 else l22 
    l3 = 1 if l33==0 else l33 
    l4 = 1 if l44==0 else l44 

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
        
        if questiondataset[i][2]>=3:
            optionclass[count]=2
        elif(questiondataset[i][2]==2):
            optionclass[count]=1
        elif(questiondataset[i][2]==1):
            optionclass[count]=0
        count +=1
    x = np.array((ans,optionclass,timeclass)).T
    y=linearreg(x)
    count=0
    for i in questiondataset:
      if questiondataset[i][0]== -1 :
        y[count]=0.01
      count +=1
    # print("Question wise p value:: " , y)

    pq['TSD']=0.0
    pq['TW']=0.0
    pq['SI']=0.0
    pq['PPL']=0.0
    # y-> 15 p
    for i in range(15):
        pq[topic[i]] += y[i]
    pq['TSD'] = 0.01 if pq['TSD']==0.0 else pq['TSD']
    pq['TW'] = 0.01 if pq['TW']==0.0 else pq['TW']
    pq['SI'] = 0.01 if pq['SI']==0.0 else pq['SI']
    pq['PPL'] = 0.01 if pq['PPL']==0.0 else pq['PPL']
    pq['TSD'] /=l1
    pq['TW'] /=l2
    pq['SI'] /=l3
    pq['PPL'] /=l4
    # print("topic wise P value is:: ", pq)
    insertPerformance(testId)
    
    # print("No of questions per topic")
    topicRt= topicRatio(pq['TSD'],pq['TW'],pq['SI'],pq['PPL'],15)
    # print(topicRt)
    topicname=['TSD','TW','SI','PPL']
    for i in range(4):
        topicLevelRt[topicname[i]]=inferenceEngine(pq[topicname[i]], topicRt[i])

    # print("No of ques of each Level in each topic")
    # print("Question params are : ",questiondataset)
    # print("Time class is : ",timeclass)
    # print("Option Class is : ", optionclass)
    # print(topicLevelRt)
    updateTopiclevelratio()
    # if(selectWhereTable1('topiclevelratio','Username',username)): 
    #   updateTopiclevelratio()
    # else:
    #   insertTopiclevelratio()  

    return redirect(url_for('profileB.profile'))

# Query

def selectWhereTable1(tableName, columnname1, columnvalue1):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get="SELECT * FROM `"+tableName+"` WHERE `"+columnname1+"` = '"+columnvalue1+"'"
    cursor.execute(get)
    account= cursor.fetchone()
    return account

def insertPerformance(testId):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    avg_p = pq['TSD'] + pq['SI'] +pq['TW'] + pq['PPL']
    avg_p /=4 #CURRENT TEST AVG P
    if( (len(testP) + 1) % 5 ==0 ):
      # current test is a checkpoint test

      a,b,c, curlevel= timelineRatio(avg_p)

      level_all= list(zip(*testP))[8]

      lastSixlevels= [curlevel] + list(level_all[0:5])
      print("lastSixLevels ", lastSixlevels)
      # lastSixlevels.insert(0, curlevel)
      print("Levels of Last five tests and current test are: ", lastSixlevels)
      
      totalP_all= list(zip(*testP))[6]
      lastFourP = totalP_all[0:4]
      print("Last four tests P values are ", lastFourP)
      # lastFiveP = testP[7][-5:]
      checkpt_avg = (sum(lastFourP) + avg_p)/5
      # AVG LEVEL FOUND HERE
      a,b,c, checkpt_level = timelineRatio(checkpt_avg)

      print("Avg P and Avg level is ", checkpt_avg, checkpt_level)
      # NO. OF CHANGEs
      changes=0
      beginner=0
      intermediate=0
      master=0
      # I B I I I B 
      # B I I I B I 

      for i in range(5):
        # Changes
        if(lastSixlevels[i+1] != lastSixlevels[i]):
          changes +=1
        # Count or frequency
        if(lastSixlevels[i] == 'Beginner'):
          beginner +=1
        elif(lastSixlevels[i] == 'Intermediate'):
          intermediate +=1
        else:
          master +=1  
      print("Changes ", changes)
      print("Freq ", beginner, intermediate, master)

      if(changes == 0 or changes == 1 or changes == 2 or changes == 3):
        # support decision of checkpt_level
        gLevel = checkpt_level
      elif(changes == 4 or changes == 5):
        # dont support
        if( master + intermediate > beginner):
          # Support
          gLevel = checkpt_level
        else:
          gLevel = lastSixlevels[0]
      print("Final Checkpoint level is ", gLevel)
    else:
      a,b,c, gLevel= timelineRatio(avg_p)
      print("Current non checkpoint test's level is ", gLevel)

    insert="INSERT INTO `performance`(`testId`, `TSD`, `TW`, `SI`, `PPL`, `testP` ,`Username`, `gLevel`) VALUES ('"+testId+"',"+str(pq['TSD'])+","+str(pq['TW'])+","+str(pq['SI'])+","+str(pq['PPL'])+","+str(avg_p)+", '"+username+"','"+ gLevel +"' )"
    cursor.execute(insert)
    connection.commit()

def insertTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    for k in topicLevelRt.keys():
        insert="INSERT INTO `topiclevelratio`(`Topic`, `Level 1`, `Level 2`, `Level 3`,`Username`) VALUES ('"+k+"',"+str(topicLevelRt[k][0])+","+str(topicLevelRt[k][1])+","+str(topicLevelRt[k][2])+", '"+username+"')"
        cursor.execute(insert)
        connection.commit()

def updateTopiclevelratio():
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    cursor=connection.cursor() 
    for k in topicLevelRt.keys():
        update="UPDATE `topiclevelratio` SET `Level 1`="+str(topicLevelRt[k][0])+",`Level 2`="+str(topicLevelRt[k][1])+",`Level 3`="+str(topicLevelRt[k][2])+" WHERE `Username`='"+username+"' AND `Topic`= '"+k+"'"
        cursor.execute(update)
        connection.commit()

#UPDATE `topiclevelratio` SET `Topic`=[value-3],`Level 1`=[value-4],`Level 2`=[value-5],`Level 3`=[value-6] WHERE `Username`=[value-2]
# Compute
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

def handleratios(result):
  count=0
  # print("Result before calcration: ", result)
  for r in result.values():
    if r==0:
      all=result.values()
      i= getkey(result, max(all))
      # i= result.index(max(result)) 
      result[i]-=1
      result[count]+=1
      # print("R was zero and now:: ",result)
    count+=1
  # print("Result is:" , result)
  return result

def getkey(lt_ftp, val):
   for key, value in lt_ftp.items(): 
     if val == value: 
       return key 

def timelineRatio(p):
  if p<=0.09 :
    a=15
    b=0
    c=0
    d="Beginner"
  elif(p<=0.19):
    a=13
    b=2
    c=0
    d="Beginner"
  elif(p<=0.29):
    a=10
    b=5
    c=0
    d="Beginner"
  elif(p<=0.39):
    a=7
    b=7
    c=1
    d="Beginner"
  elif(p<=0.49):
    a=5
    b=8
    c=2
    d="Intermediate"
  elif(p<=0.59):
    a=3
    b=10
    c=2
    d="Intermediate"
  elif(p<=0.69):
    a=2
    b=8
    c=5
    d="Intermediate"
  elif(p<=0.79):
    a=2
    b=5
    c=8
    d="Master"
  elif(p<=0.89):
    a=1
    b=3
    c=11
    d="Master"
  elif(p<=1):
    a=0
    b=0
    c=15
    d="Master"
  else:
    a=1
    b=1
    c=1
    d=""
  return a,b,c,d

def inferenceEngine(p, totalq):
  levelRt=dict()
  # Ratio of levels for a particular topic
  a,b,c,d = timelineRatio(p)
  tmp=findRatioLevel(a,b,c,totalq)
  levelRt=findIntRatio(tmp, totalq)
  # levelRt[0]=tmp[0]
  # levelRt[1]=tmp[1]
  # levelRt[2]=tmp[2]
  return levelRt


def topicRatio(pt1,pt2,pt3,pt4,totalq):
  # a:b:c:d -> 0.5:0.75:0.3:0.1
  # den= a+b+c+d
  # a/den*15:b/den*15 ...
  topicRt= dict()
  tmp=findRatioTopic(pt1,pt2,pt3,pt4,totalq)
  topicRt= findIntRatio(tmp,totalq)
  handleratio=handleratios(topicRt)
  return handleratio