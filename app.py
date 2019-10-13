# from flask import Flask
import pymysql

# def selectquery():
#     retrieve="Select * from student"
#     cursor.execute(retrieve)

#     print('SELECT')
#     rows= cursor.fetchall()
#     for row in rows:
#         print(row)

# # database connection
# connection= pymysql.connect(host="localhost",user="root",passwd="",database="gjstrial")
# cursor=connection.cursor()

# # queries
# # retrieve="Select * from `question data` where `question no`=3;"
# selectquery()

# insert="Insert into student values('abc','1234','abc@gmail.com')"
# cursor.execute(insert)
# print("After INSERT")
# selectquery()

# #commiting the connection then closing it. Otherwise the updated change is unsaved
# connection.commit()
# connection.close()

app=Flask(__name__)

@app.route('/')
def hello():
    return render.template('')

if __name__ == "__main__":
    app.run()

    