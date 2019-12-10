from flask import Flask, render_template,json
import pymysql

def selectquery():
    retrieve="Select * from `question data` "
    cursor.execute(retrieve)

    # print('SELECT')
    rows= cursor.fetchall()
    # print(rows[0][1])
    return rows
    # for row in rows:
    #     print(row)

# database connection
connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
cursor=connection.cursor()

# queries
# retrieve="Select * from `question data` where `question no`=3;"
# selectquery()

# insert="Insert into student values('abc','1234','abc@gmail.com')"
# cursor.execute(insert)
# print("After INSERT")
# selectquery()


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/test')
def test():
    rows=selectquery()
    #print(type(rows))
    return render_template('test.html',value=rows)
# Sends all rows as value, possible due to render template

if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port=5000, debug=True)

#commiting the connection then closing it. Otherwise the updated change is unsaved
connection.commit()
connection.close()