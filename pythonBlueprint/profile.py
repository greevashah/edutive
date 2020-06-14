from flask import Flask,Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime 
import pymysql
import requests
# from pythonBlueprint.thanking import timelineRatio
profileB=Blueprint('profileB',__name__)

# TestID
@profileB.route('/profile') 
def profile():
    global showProfile, values, testP
    u= session['username']
    values= selectWhereTableOrder('testdataset', 'Username', u)
    # print(values['testP'])
    accuracy_all= list(zip(*values))[6]
    avg_accuracy= sum(accuracy_all)/ len(values)
    print("AVG Accuracy is ", avg_accuracy)

    testP = selectWhereTableOrder('performance', 'Username', u)
    showProfile= True 
    profileLevel = len(testP) % 5
    levels_all= list(zip(*testP))[8]
    print("Levels of all tests: ", levels_all)
    if( len(testP) < 5):
        last_level = levels_all[len(testP) - 1 ]
    else:
        last_level = levels_all[profileLevel]

    if(last_level == 'Beginner'):
        width=30
    elif(last_level == 'Intermediate'):
        width=60
    else:
        width=90
    
    TSD_all= list(zip(*testP))[2]
    TSD_P= int(sum(TSD_all)/ len(values) *100)
    TW_all= list(zip(*testP))[3]
    TW_P= int(sum(TW_all)/ len(values) *100)
    SI_all= list(zip(*testP))[4]
    SI_P= int(sum(SI_all)/ len(values) *100)
    PPL_all= list(zip(*testP))[5]
    PPL_P= int(sum(PPL_all)/ len(values) *100)

    print("Last level ", last_level)

    checkpoint= timeline(values,testP)

    # levels= findTestLevel(testP)
    # a, b, c, d = timelineRatio(p)
    return render_template('profile.html', name= u , value=values, showProfile= showProfile, avg_accuracy= avg_accuracy, last_level= last_level, progress_width= width,TSD_P= TSD_P, TW_P= TW_P , SI_P= SI_P , PPL_P= PPL_P , checkpoint=checkpoint) 

def selectWhereTableOrder(tableName, columnname, columnvalue):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' ORDER BY `testId` desc "
    cursor.execute(get1)
    rows= cursor.fetchall()
    return rows

@profileB.route('/tp/<testID>')
def tp(testID):
    # return requests.post(url_for('resdis.dashboard'), testId=testID, Username= session['name'])
    # requests.post('http://localhost:5000/dashboard', data= { 'testId': testID, 'Username': session['name'] } , allow_redirects= True)
    s=session['username']
    sP= request.args.get('showProfile')
    if sP == "false":
        print("HEREEEEEE")
        sP= False
        # sp=True
    print("showProfile from tp route: ", sP)
    # else:
    #     sP=showProfile
    #     print("showProfile from tp route outside IF: ", sP)

    # if analysis == True:
    #     # View details, only for analysis purpose
    # else:
    #     # Show finish button
    return redirect(url_for('resdis.dashboard', testId=testID, username=s, showProfile= sP )) 

@profileB.app_template_filter('ctime')
def timestamptotime(testID):
    timestamp = int(testID)
    dt_object = datetime.fromtimestamp(timestamp)
    # print(dt_object)
    return dt_object


def timeline(values1, testP1):
    global checkpoint 
    acc = 0  
    scr = 0 
    time = 0
    checkpoint = []
    values= values1[::-1]
    testP = testP1[::-1]
    print("Values " , values ) 
    print("testP " , testP ) 
    # 0 to 9 
    for i in range(len(values)):
        #if loop 4 
        if (i+1) % 5 == 0: 
            acc+= values[i][6] 
            scr+= values[i][4] 
            timeT = timetosec(values[i][1])
            time+= timeT
            acc = acc/5
            scr = scr/5
            time = time/5
            xyz = [acc, scr , time]
            xyz.append(testP[i][8])
            checkpoint.append(xyz)
            print("checkpoint is " , checkpoint)
            acc = 0
            scr = 0 
            time = 0
        else:
            acc+= values[i][6] 
            scr+= values[i][4] 
            timeT = timetosec(values[i][1])
            time+= timeT  
    return checkpoint
         
def timetosec(timestr):
    time = int(timestr.split(':')[0])*60*60 + int(timestr.split(':')[1])*60 + int(timestr.split(':')[2])
    print(time)
    return time




