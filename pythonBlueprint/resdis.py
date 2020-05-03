from flask import Flask,Blueprint, render_template, request
# from models import query
# import requests
from decimal import *
import pymysql
 
resdis=Blueprint('resdis',__name__)

# TestID

@resdis.route('/dashboard/<testId>') #selectWhereTable selectTestScore
def dashboard(testId):
    username= request.args.get('username')
    # print("Name is "+ )
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
    return render_template('dashboard.html', value=ds, value1=newRow, value2=testds, value3= testId, name= username)

#One condition
def selectWhereTable(tableName, columnname, columnvalue):
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")  
    cursor=connection.cursor()      
    get1="SELECT * FROM `"+tableName+"` WHERE `"+columnname+"` = '"+columnvalue+"' "
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


@resdis.route('/result') #selectWhereTable
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
