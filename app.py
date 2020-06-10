from flask import Flask,Blueprint,render_template,json,request
import os
import pymysql

app=Flask(__name__)

# database connection
# connection= pymysql.connect(host="eu-cdbr-west-03.cleardb.net",user="b72668611cc1ee",passwd="822351e1",database="heroku_279e13e2a650fcd" , connect_timeout=60000)
# connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")


from pythonBlueprint.test import testB
app.register_blueprint(testB)

from pythonBlueprint.thanking import thankingB
app.register_blueprint(thankingB)

from pythonBlueprint.sendparam import send
app.register_blueprint(send)

from pythonBlueprint.resdis import resdis
app.register_blueprint(resdis)

from pythonBlueprint.user import user
app.register_blueprint(user)

from pythonBlueprint.profile import profileB
app.register_blueprint(profileB)

# ROUTING
@app.route('/')
def index():
    # session['loggedIn']=False
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    return render_template('landing.html')

if __name__ == "__main__":
    app.secret_key="secret"
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=port, debug= True)
