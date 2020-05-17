from flask import Flask,Blueprint, render_template, session, redirect, url_for
from datetime import datetime
import pymysql
import requests

profileB=Blueprint('profileB',__name__)

# TestID
@profileB.route('/profile') 
def profile():
    s= session['name']
    u= session['username']
    values= selectWhereTableOrder('testdataset', 'Username',u)
    return render_template('profile.html', name= s , value=values) 

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
    s=session['name']
    return redirect(url_for('resdis.dashboard', testId=testID, username=s)) 

@profileB.app_template_filter('ctime')
def timestamptotime(testID):
    timestamp = int(testID)
    dt_object = datetime.fromtimestamp(timestamp)
    print(dt_object)
    return dt_object



