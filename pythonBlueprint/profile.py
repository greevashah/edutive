from flask import Flask,Blueprint, render_template, session, redirect, url_for
import requests

profileB=Blueprint('profileB',__name__)

# TestID
@profileB.route('/profile') 
def profile():
    s= session['name']
    return render_template('profile.html', name= s)

@profileB.route('/tp/<testID>')
def tp(testID):
    # return requests.post(url_for('resdis.dashboard'), testId=testID, Username= session['name'])
    # requests.post('http://localhost:5000/dashboard', data= { 'testId': testID, 'Username': session['name'] } , allow_redirects= True)
    s=session['name']
    return redirect(url_for('resdis.dashboard', testId=testID, username=s))