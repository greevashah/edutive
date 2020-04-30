from flask import Flask,Blueprint, render_template
from models.query import insertTopiclevelratio, insertPerformance
from models.computation import topicRatio , inferenceEngine

thankingB=Blueprint('thankingB',__name__)

@thankingB.route('/thanking') # insertPerformance() topicRatio inferenceEngine insertTopiclevelratio()
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
