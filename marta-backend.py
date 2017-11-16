# Function to see whether login works
# Goes with VerifyLogin function in login_screen window

def VerifyLogin(self):	
	username = str(self.usernameTextEdit.toPlainText())
    password = str(self.passwordTextEdit.toPlainText())
    import pymysql
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
    							user = 'cs4400_Group_110',
    							password = 'KAfx5IQr',
    							db = 'cs4400_Group_110')
    try:
    	with connection.cursor() as cursor:
    		# We have to somehow hash the password to make sure it's the same in the database
    		sql = """SELECT Username as U, Password as P FROM User
    				WHERE username = U and password = P"""
    		cursor.execute(sql)
    except:
    	# Some sort of error message goes here
    finally:
    	connection.close()
    	# print("Done") #For testing purposes only