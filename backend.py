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
    		sql = 'SELECT * FROM User WHERE Username = {} and Password = {}'.format(username, hashlib.md5(password).hexdigest())
    		cursor.execute(sql)
            global is_admin
            is_admin = bool(cursor.fetchall()[2])
            return 1 if cursor.fetchall() else -1 # 1 if successful, -1 if unsuccessful
    except:
    	print("This should have worked. Blame Joel")
    finally:
    	connection.close()
    	# print("Done") #For testing purposes only
