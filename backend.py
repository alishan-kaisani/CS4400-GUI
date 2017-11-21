# Function to see whether login works
# Goes with VerifyLogin function in login_screen window

import pymysql
import hashlib
from random import randrange

def VerifyLogin(self):	
	username = str(self.usernameTextEdit.toPlainText())
    password = str(self.passwordTextEdit.toPlainText())
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
    							user = 'cs4400_Group_110',
    							password = 'KAfx5IQr',
    							db = 'cs4400_Group_110')
    try:
    	with connection.cursor() as cursor:
    		# We have to somehow hash the password to make sure it's the same in the database
    		sql = 'SELECT * FROM User WHERE Username = "{}" and Password = "{}"'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest())
    		cursor.execute(sql)
            global is_admin
            is_admin = bool(cursor.fetchall()[0][2]) if cursor.fetchall() else None
            # Open a new window if login is successful
            # You can do this with the following code:
            # if cursor.fetchall():
            # Open new window here
            return 1 if cursor.fetchall() else -1 # 1 if successful, -1 if unsuccessful
    except:
    	print("This should have worked. Blame Joel")
    finally:
    	connection.close()
    	# print("Finished login query") #For testing purposes only

def GenerateNewCardNumber():
    while True:
        newnum = randrange(int(1e15), int(1e16))
        sql = 'SELECT * FROM Breezecard WHERE BreezecardNum = "{}"'.format(newnum)
        connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                user = 'cs4400_Group_110',
                                password = 'KAfx5IQr',
                                db = 'cs4400_Group_110')
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.close()
        if len(result) == 0:
            return newnum

def CreateNewUser(username, email, password, cardnumber=None): #cardnumber may be either a string or a 16-digit integer
    if cardnumber is None:
        cardnumber = GenerateNewCardNumber()
    assert len(str(cardnumber)) == 16, "Card number must be 16 digits"
    sql = 'INSERT INTO User VALUES ("{}", "{}", false)'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest()) #New users are always passengers, not admins
    sql2 = 'INSERT INTO Passenger VALUES ("{}", "{}")'.format(username, email)
    sql3 = 'INSERT INTO Breezecard VALUES ("{}", 0.00, "{}")'.format(cardnumber, username)
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                user = 'cs4400_Group_110',
                                password = 'KAfx5IQr',
                                db = 'cs4400_Group_110')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
            cursor.execute(sql2)
            connection.commit()
            cursor.execute(sql3)
            connection.commit()
            # Tell the GUI to do something (if necessary)
            return 1
   # except:
    #        print("Something went wrong. Blame Joel")
    finally:
        connection.close()
        # print("Finished creating new user") #For testing purposes only
