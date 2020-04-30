import random
from models.query import selectTopicLevelTable
# COMPUTATION FUNCTIONS

# Computing topicQ and timept dictionaries
def computeRows(qnum,elapt): 
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
