# Function to see whether login works
# Goes with VerifyLogin function in login_screen window

import pymysql
import hashlib

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

def CreateNewUser(username, password):
    sql = 'INSERT INTO User VALUES ("{}", "{}", false)'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest()) #New users are always passengers, not admins
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                user = 'cs4400_Group_110',
                                password = 'KAfx5IQr',
                                db = 'cs4400_Group_110')
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
            # Tell the GUI to do something if necessary
	    return 1
    except:
            print("Something went wrong. Blame Joel")
    finally:
        connection.close()
        # print("Finished creating new user") #For testing purposes only
