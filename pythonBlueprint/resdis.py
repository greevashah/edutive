from flask import Flask,Blueprint, render_template
from models import query
 
resdis=Blueprint('resdis',__name__)


@resdis.route('/dashboard') #selectWhereTable selectTestScore
def dashboard():
    ds= query.selectWhereTable("dataset","testId",testId)
    topicds=query.selectWhereTable("topicdataset","testId",testId)
    # testds=selectWhereTable("testdataset","testId",testId)
    testds=query.selectTestScore()
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


@resdis.route('/result') #selectWhereTable
def result():
    # print("Here in result")
    ds= query.selectWhereTable("dataset","testId",testId)
    topicds=query.selectWhereTable("topicdataset","testId",testId)
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
