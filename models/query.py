import pymysql

def connectionF(): 
    connection= pymysql.connect(host="localhost",user="root",passwd="",database="berang")
    return connection
  
# FUNCTIONS 
# Query functions


# def selecttopic1():
#     get1="SELECT * FROM `questiondata` WHERE `Difficulty` IN ('Level 1' , 'Level 2') AND `Topic` ='TSD' "
#     cursor.execute(get1)
#     rows1= cursor.fetchall()
#     return rows1
