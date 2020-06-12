from flask import Flask,Blueprint, render_template, session, redirect, url_for, request
from datetime import datetime
import pymysql
import requests
from pythonBlueprint.thanking import timelineRatio
profileB=Blueprint('profileB',__name__)

# TestID
@profileB.route('/profile') 
def profile():
    global showProfile
    u= session['username']
    values= selectWhereTableOrder('testdataset', 'Username',u)
    testP = selectWhereTableOrder('performance', 'Username',u)
    showProfile= True
    # a, b, c, d = timelineRatio(p)
    return render_template('profile.html', name= u , value=values, showProfile= showProfile) 

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
    print(dt_object)
    return dt_object



