from flask import Flask,Blueprint, render_template, request
from models.query import insertTopicDataset , insertDataset , insertTestDataset
from models.computation import convertToIntList , computeRows, computeTopicwise

send=Blueprint('send',__name__)



@send.route('/sendparameters',methods=['POST']) #convertToIntList computeRows() insertDataset() computeTopicwise() insertTopicDataset() insertTestDataset()
def get_data():
    global qnum,ans,optch,elapt,totaltime,totalcorrect,totalincorrect,testscore
    qnum=convertToIntList(request.form['questions'])
    ans=convertToIntList(request.form['answers'])
    # print(type(arr1))
    optch=convertToIntList(request.form['optionchanges'])
    # print(arr2)
    elapt=convertToIntList(request.form['elapsedtime'])
    # print(arr3)
    totaltime=request.form['totalTimeTaken']
    # print(type(arr4))
    totalcorrect=request.form['totalcorrect']
    totalincorrect=request.form['totalincorrect']
    testscore=request.form['testscore']
    computeRows(qnum,elapt)
    insertDataset()
    computeTopicwise()
    insertTopicDataset()
    insertTestDataset()
    print("Leaving sendparameters")
    return "lol"
