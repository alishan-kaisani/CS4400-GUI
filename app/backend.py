import pymysql
import hashlib
from random import randrange
from datetime import datetime
import sys
import string

#Leaving a note here for future reference: 
#global vars:
# is_admin
# passenger_username

def VerifyLogin(gui_username, gui_password):
	"""Determine whether a logon attempt is valid by querying the database.
	If the logon attempt is successful, is_admin becomes a global variable for use later on.
	is_admin is either True or False, depending on whether the user is an administrator.
	The function returns 1 if the logon attempt is successful or -1 if unsuccessful."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	try:
		with connection.cursor() as cursor:
			# We have to somehow hash the password to make sure it's the same in the database
			sql = 'SELECT * FROM User WHERE Username = "{}" and Password = "{}";'.format(gui_username, hashlib.md5(gui_password.encode('utf-8')).hexdigest())
			cursor.execute(sql)
			m = cursor.fetchall()
			global is_admin
			is_admin = bool(m[0][2]) if m else None
			global passenger_username
			passenger_username = gui_username
			return 1 if m else -1 # 1 if successful, -1 if unsuccessful
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()
		# print("Finished login query") #For testing purposes only

def Logout():
	"""Logs the user out of the system.
	The user's is_admin and passenger_username global variables are set to None so that the memory of the user is gone from the system."""
	is_admin = None
	passenger_username = None
	# Open login screen in GUI

def GenerateNewCardNumber():
	"""Randomly generates new breezecard values for use in CreateNewUser function, when necessary.
	Returns a 16-digit integer that is not already in the database."""
	while True:
		newnum = randrange(int(1e15), int(1e16))
		sql = 'SELECT * FROM Breezecard WHERE BreezecardNum = "{}";'.format(newnum)
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

def EnsureIsEmail(email):
	"""Ensure that a given input (email (str)) is in a valid email format.
	Returns True or False."""
	mylist = email.split("@")
	if len(mylist) != 2:
		return False
	for char in mylist[0]:
		if char not in (string.ascii_letters + string.digits + '.'):
			return False
	for char in mylist[1]:
		if char not in (string.ascii_letters + string.digits + '.'):
			return False
	return (mylist[1][-1] != '.' and mylist[1][0] != '.' and '.' in mylist[1])

def CreateNewUser(username, email, password, cardnumber=None):
	"""Adds a new user to the database; inserts tuples into User, Passenger, and Breezecard tables.
	Returns 1 if the operation is successful, otherwise an exception is raised."""
	if cardnumber is None:
		cardnumber = GenerateNewCardNumber()
	if not EnsureIsEmail(email):
		# GUI error because the email address as entered is not of a valid email format
		return "Bad Email"
	sql = 'INSERT INTO User VALUES ("{}", "{}", false);'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest()) 
	#New users are always passengers, not admins
	sql2 = 'INSERT INTO Passenger VALUES ("{}", "{}");'.format(username, email)
	sql3 = 'INSERT INTO Breezecard VALUES ("{}", 0.00, "{}");'.format(cardnumber, username)
	sql_query = 'SELECT * FROM Breezecard WHERE BreezecardNum="{}";'.format(cardnumber)
	sql_if_needed = 'INSERT INTO Conflict VALUES ("{}", "{}", CURRENT_TIMESTAMP);'.format(username, cardnumber)
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
			cursor.execute(sql_query)
			m = cursor.fetchall()
			if not m:
				cursor.execute(sql3)
				connection.commit()
			else:
				cursor.execute(sql_if_needed)
				connection.commit()
			# Tell the GUI to do something (if necessary)
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def CreateNewUserWrapper(existing_card, username, email, password, *args):
	"""Calls the CreateNewUser function depending on whether the new user is using an existing Breeze Card or wishes to generae a new one.
	existing_card is a boolean parameter that determines whether the new user already has a breezecard.
	username, email, and password have the same meaning as they do in CreateNewUser.
	*args allows for the optional parameter (Breeze Card number) to be called when existing_card == True.
	Returns 1 if successful, otherwise an exception is raised."""
	if existing_card == False:
		return CreateNewUser(username, email, password)
	else:
		return CreateNewUser(username, email, password, args[0])
	# The CreateNewUser function will return 1, so we do not need to include a return statement in this function

def AddBreezeCard(cardnum):
	"""A user inputs a Breeze card number and makes it theirs. The card must exist somewhere in the database.
	Returns 1 to indicate success.
	A user inputs a Breeze card number and makes it theirs. The card must exist somewhere in the database."""
	sql = 'UPDATE Breezecard SET BelongsTo="{}" WHERE BreezecardNum="{}";'.format(passenger_username, cardnum)
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def RemoveCard(cardnum):
	"""Disassociate a user from a breeze card.
	Returns 1 to indicate success"""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Breezecard SET BelongsTo=null WHERE BreezecardNum="{}";'.format(cardnum)
	try:
		with connection.cursor() as cursor:
			print(sql)
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def AddValue(cardnum, value):
	"""cardnum (str) and value (float) are self-explanatory.
	User adds value to his or her card"""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql_first = 'SELECT Value FROM Breezecard WHERE BreezecardNum="{}";'.format(cardnum)
	with connection.cursor() as cursor:
		cursor.execute(sql_first)
		current_value = float(str(cursor.fetchall()[0][0]))
	sql = 'UPDATE Breezecard SET Value={} WHERE BreezecardNum="{}";'.format(value + current_value, cardnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ViewStations(orderBy='Name'):
	"""Returns a tuple of tuples, where each nested tuple is of the form (Station name, StopID, Decimal('fare amount'), ClosedStatus).
	orderBy (str) is a string that is one of 'Name', 'StopID', 'EnterFare', 'ClosedStatus'; orderBy is assigned 'Name' by default
	If tuple not returned, then exception would have been raised.
	Use the PrettifyViewStations() function to get rid of annoying """
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Name, StopID, EnterFare, ClosedStatus FROM Station ORDER BY {} ASC;'.format(orderBy)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			return m
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def PrettifyViewStations(orderBy='Name'):
	"""Makes the station listing from the ViewStations() function usable, since each station's fare will no longer be a Decimal object.
	orderBy (str) takes the same values and has the same meaning as in the ViewStations() function.
	Returns a list of several tuples where the Decimal object is replaced by a floating point number (otherwise an exception would have been raised)."""
	listing = ViewStations(orderBy)
	newlisting = []
	for tup in listing:
		if tup[3] == 1:
			newlisting.append((tup[0], tup[1], round(float(tup[2]), 2), "Closed"))
		else:
			newlisting.append((tup[0], tup[1], round(float(tup[2]), 2), "Open"))
	return newlisting

def ViewAllBusStations():
	"""Return a list of all bus stations, where each bus station is a tuple of the form (Name, StopID, fare, ClosedStatus, NearestIntersection).
	The function only shows stations that are open."""
	sql = 'SELECT Name, StopID, EnterFare FROM Station WHERE ClosedStatus=0 and isTrain=0 ORDER BY NAME;'
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			mylist = []
			for tup in m:
				mylist.append((tup[0], tup[1], float(tup[2])))
			return mylist
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ViewAllTrainStations():
	"""Return a list of all train stations, where each train station is a tuple of the form (Name, StopID, fare, ClosedStatus).
	This function only shows stations that are open."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Name, StopID, EnterFare FROM Station WHERE IsTrain=1 AND ClosedStatus=0 ORDER BY Name;'
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			mylist = []
			for tup in m:
				mylist.append((tup[0], tup[1], float(tup[2])))
			return mylist
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

#EDIT: I added IsTrain to the query bc I need it to format the station detail page
def ViewSingleStation(stopID):
	"""Returns a tuple with information on a single station.
	stopID (str) is self-explanatory and the primary key of the database."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Name, StopID, EnterFare, ClosedStatus, IsTrain FROM Station WHERE stopID="{}";'.format(stopID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchone()
			return (m[0], m[1], float(m[2]), m[3], m[4]) if m else ()
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ViewIntersection(stopID):
	"""Return a list of one tuple of the form (StopID, Nearest Intersection) for a specific station."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Intersection FROM BusStationIntersection WHERE StopID="{}";'.format(stopID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchone()
			return m[0]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def CreateTrainStation(stationName, stopID, entryFare, closedStatus):
	"""Creates a new train station by inserting a tuple into the Station table.
	stationName (str), stopID (str), and entryFare (float) all have fairly obvious meanings.
	closedStatus is 1 if True or 0 if False (may take int or bool value)
	Function returns 1 if successful or returns None and prints an error message to the console if an exception is raised."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	closedStatus = 'true' if closedStatus in (1, True) else 'false' if closedStatus in (0, False) else None
	sql = 'INSERT INTO Station VALUES ("{}", "{}", {}, {}, true);'.format(stopID, stationName, entryFare, closedStatus)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def CreateBusStation(stationName, stopID, entryFare, closedStatus, *args):
	"""Creates a new bus station by inserting a tuple into the Station table and, if appropriate, the BusStationIntersection table.
	stationName (str), stopID (str), entryFare (float), closedStatus (bool or float) all have fairly obvious meanings.
	*args creates args (tuple) variable, which will have exactly 0 or 1 elements.
	If args has one element, then that element will be the nearest intersection (str).
	Function returns 1 or prints error message to console whilst returning None."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	closedStatus = 'true' if closedStatus in (1, True) else 'false' if closedStatus in (0, False) else None
	if args[0] == '':
		args = ()
	sql = 'INSERT INTO Station VALUES ("{}", "{}", {}, {}, false);'.format(stopID, stationName, entryFare, closedStatus)
	if args:
		sql2 = 'INSERT INTO BusStationIntersection VALUES ("{}", "{}");'.format(stopID, args[0])
	else:
		sql2 = 'INSERT INTO BusStationIntersection VALUES ("{}", null);'.format(stopID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			cursor.execute(sql2)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def CreateStationWrapper(isTrain, stationName, stopID, entryFare, closedStatus, *args):
	"""Wrapper function for creating new station.
	isTrain (bool) determines whether the new station is a train station.
	*args creates variable args (tuple) with 0 or 1 elements (that element, if it exists, is a string of the nearest intersection for bus stations only).
	Parameters stationName (str), stopID (str), entryFare (float), and closedStatus (bool or int) have the same meaning as before."""
	if isTrain:
		return CreateTrainStation(stationName, stopID, entryFare, closedStatus)
	elif not args:
		return CreateBusStation(stationName, stopID, entryFare, closedStatus)
	else:
		return CreateBusStation(stationName, stopID, entryFare, closedStatus, args[0])

#EDIT: This function does return tuples in the order described here
# DB is returning (username,breezecard#,datetime,username) -> This query needs to be double checked
# Prettify was adjusted to match expected ordr
def ViewSuspendedCards(): #MUST BE UPDATED WITH JOIN IN QUERY TO GET CURRENT OWNER
	"""Returns a tuple of tuples of rows from the Conflict table.
	Each tuple is of the form (BreezecardNum (str), New Owner (str), DateTime (datetime.datetime), Previous Owner).
	Previous owner is the original owner of Breezecard, whereas New owner is the person trying to take their Breezecard."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Username, Conflict.BreezecardNum, DateTime, BelongsTo FROM Conflict LEFT OUTER JOIN Breezecard ON Conflict.BreezecardNum=Breezecard.BreezecardNum ORDER BY DateTime;'
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			return m
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

#EDIT: Let's also convert 24 datetimes into am/pm datetimes for consistency with project doc
def PrettifyViewSuspendedCards():
	"""Returns a list of tuples of rows from the ViewSuspendedCards() function query that is manageable.
	The datetime.datetime objects returned from ViewSuspendedCards are now strings that are manageable."""
	listing = ViewSuspendedCards()
	newlisting = []
	for tup in listing:
		newlisting.append((tup[1], tup[0], str(tup[2]), tup[3]))
	return newlisting

def ChangeStationClosedStatus(stopID, status):
	"""Change whether a station is open or closed.
	stopID (str) is self-explanatory.
	Function returns 1 to indicate success."""
	staus = 0
	if status:
		status = 1
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Station SET ClosedStatus="{}" WHERE StopID="{}";'.format(status,stopID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ChangeStationFare(stopID, newFare):
	"""Change the fare of a station.
	stationID (str) and newFare (float) are pretty self-explanatory.
	newFare will always be rounded to two decimal places to avoid against poorly or maliciously constructed input.
	Function returns 1 to indicate success."""
	newFare = round(newFare, 2)
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Station SET EnterFare={} WHERE StopID="{}";'.format(newFare, stopID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ChangeStation(stopID, closedStatus, newFare):
	"""Wrapper function for updating stations.
	closedStatusChange (bool) determines whether to change the closedStatus of a station.
	newFare (bool or float) determines whether to change the fare at a station and if so, to what value.
	Returns 1 to indicate success."""
	check1 = ChangeStationClosedStatus(stopID, closedStatus)
	check2 = ChangeStationFare(stopID, newFare)
	if check1 != 1:
		return check1
	if check2 != 1:
		return check2
	else:
		return 1

def SetCardValue(cardNumber, newValue):
	"""Updates the Breezecard table with new value of selected Breezecard.
	cardNumber (str) and newValue (float) are the inputs with fairly obvious meanings.
	Function returns 1 if successful or will print an error message to the console whilst returning None."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Breezecard SET Value={} WHERE BreezecardNum="{}";'.format(newValue, cardNumber)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def AssignCardToOwner(cardNumber, newOwner):
	"""Updates the Breezecard table with the new owner of selected Breezecard.
	cardNumber (str) and newOwner (str) have fairly obvious meanings.
	Function returns 1 if successful or prints error message to console (whilst returning None)."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Breezecard SET BelongsTo="{}" WHERE BreezecardNum="{}";'.format(newOwner, cardNumber)
	sql2 = 'DELETE FROM Conflict WHERE BreezecardNum="{}";'.format(cardNumber)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			cursor.execute(sql2)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def GetAllBreezeCardsOfPassenger():
	"""Return a list of tuples of all a user's breezecards (except those that are suspended).
	There are no parameters because passenger_username is always the username of the individual using the GUI at a given time."""
	sql = 'SELECT BreezecardNum FROM Breezecard WHERE BelongsTo = "{}" AND BreezecardNum NOT IN (SELECT BreezecardNum FROM Conflict);'.format(passenger_username)
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			return [x[0] for x in m]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def DTTUS(dt):
	"""Heper function to take a datetime.datetime object and convert it into a string (return type) that SQL can deal with.
	dt (datetime.datetime) is the input and it is the datetime object that needs converting.
	DTTUS stands for DateTime To Usable String."""
	return str(dt).replace('-', '/')[:19]

def TripHistoryOfUser(startTime, endTime):
	"""Return a list of tuples of trips of a user during a specified time interval (among all their Breezecards).
	startTime (datetime.datetime), and endTime (datetime.datetime) are self-explanatory input parameters.
	The user will always be passenger_username (the global variable), so we do not need an input parameter for user.
	The tuples in the list are of the form (BreezecardNum, Value, Username, Fare, StartTime, StartsAt, EndsAt)."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT StartTime, StartsAt, EndsAt, Tripfare, BreezecardNum FROM Breezecard NATURAL JOIN Trip WHERE BreezecardNum in (SELECT BreezecardNum FROM Breezecard WHERE BelongsTo="{}") AND ("{}" <= StartTime) AND (StartTime <= "{}");'.format(passenger_username, DTTUS(startTime), DTTUS(endTime))
	try:
		with connection.cursor() as cursor:
			main_list = []
			cursor.execute(sql)
			m = list(cursor.fetchall())
			return [(x[0], x[1], x[2], str(x[3]), x[4]) for x in m]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

#EDIT: I need startTime and endTime as well, I'm not filtering anything
#Removed those two inputs and from use in function
def TripHistorySingleBreezecard(bnum):
	"""Return a list of tuples of all trips associated with a specific Breezecard.
	bnum (stra) is Breezecard number, startTime (datetime.datetime) and endTime (datetime.datetime) are self-explanatory
	The tuples in the list are of the form (BreezecardNum, Value, Username, Fare, StartTime, StartsAt, EndsAt)."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT * FROM Breezecard NATURAL JOIN Trip WHERE (BreezecardNum="{}") ORDER BY StartTime DESC;'.format(bnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = list(cursor.fetchall())
			return m
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

#EDIT: Changed defulat maxValue to 1000.00 bc that's what front end is doing anyway
#Cards Can be unassigned v. Suspended; a None value doesn't automatically imply suspension
def BreezecardSearch(username='', cardNumber='', minValue=0, maxValue=1000.00, showSuspended=False):
	"""Return a list of tuples breezecards where tuples are of the form (BreezecardNum, Value, Owner)
	username (str) cardNumber (str) must be included but may be empty strings.
	minValue (float or str) maxValue (float or str) are both optional since their defaults are the min and max allowable values of Breezecards.
	showSuspended (bool) determines wheter the query will show suspended Breezecards; default value False."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	if len(cardNumber) not in (0, 16):
		return "Card number must be 16 digits long or an empty string; do not use spaces or non-numeric characters"
	sql = 'SELECT * FROM Breezecard WHERE (BreezecardNum NOT IN (SELECT BreezecardNum FROM Conflict)) AND ({} <= Value) AND (Value <= {});'.format(minValue, maxValue)
	sql2 = 'SELECT BreezecardNum, Value, Username FROM Conflict NATURAL JOIN Breezecard;'
	if username != '':
		sql = sql[:-1] + ' AND (BelongsTo = "{}");'.format(username)
	if cardNumber != '':
		sql = sql[:-1] + ' AND (BreezecardNum = "{}");'.format(cardNumber)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			cursor.execute(sql2)
			n = cursor.fetchall()
			if not showSuspended:
				return [(x[0], round(float(x[1]), 2), 'Unassigned' if x[2]==None else x[2]) for x in m]
			elif username != '' and showSuspended:
				return [(x[0], round(float(x[1]), 2), 'Unassigned' if x[2]==None else x[2]) for x in m]
			elif cardNumber != '' and showSuspended:
				return [(x[0], round(float(x[1]), 2), 'Unassigned' if x[2]==None else x[2]) for x in m]
			elif showSuspended:
				return [(x[0], round(float(x[1]), 2), 'Suspended' if x[0] in [p[0] for p in n] else 'Unassigned' if x[2]==None else x[2]) for x in n+m]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

# POSSIBLE FIX: Make query so that it does not show suspended cards
def ViewPassengerCards():
	"""View all the breezecards of a passenger and the associated values associated with the breesecards.
	Returns a list of tuples from the database of the form (BreezecardNum, Username)."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT BreezecardNum, Value FROM Breezecard where BelongsTo="{}";'.format(passenger_username)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			return [(x[0], float(x[1])) for x in m]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def ViewPassengerFlowReport(startTime=datetime(2017, 10, 10, 11, 0, 0, 0), endTime=datetime.now()):
	"""View the passenger flow report for all stations.
	Returns a list of tuples of the form (StationName, # In, # Out, Flow, Revenue)
	startTime (datetime.datetime) and endTime (datetime.datetime) are self-explanatory."""
	sql = """SELECT (

SELECT Name
FROM Station
WHERE Station.StopID = StartsAt
), COUNT( StartsAt ) , (

SELECT COUNT( * ) 
FROM Trip AS T2
WHERE T1.StartsAt = T2.EndsAt
), COUNT( StartsAt ) - ( 
SELECT COUNT( * ) 
FROM Trip AS T2
WHERE T1.StartsAt = T2.EndsAt ) , SUM( TripFare ) 
FROM Trip AS T1
WHERE T1.StartTime
BETWEEN  "{}"
AND  "{}"
GROUP BY StartsAt;""".format(DTTUS(startTime), DTTUS(endTime)).replace("\n", " ")
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchall()
			return [(x[0], x[1], x[2], x[3], float(x[4])) for x in m]
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def BreezeCardMoney(cardnum):
	"""Return the amount of money on a breeze card (float).
	Input is cardnum (str), which must be 16 digits long and have no spaces (all digits).
	It is not checked to make sure that there are 16 digits in the breezecard, as it will be assumed that the input comes straight from the GUI, not a human."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'SELECT Value FROM Breezecard WHERE BreezecardNum="{}";'.format(cardnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			m = cursor.fetchone()
			return float(m[0])
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def EndTrip(cardnum, stopID):
	"""End a user's trip taken on a specified Breeze Card.
	cardnum (str) is self-explanatory; stopID (str) is the station ID of the ending destination.
	Returns 1 to indicate success."""
	if not PassengerInTrip():
		return "Passenger not already in trip"
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	sql = 'UPDATE Trip Set EndsAt="{}" WHERE BreezecardNum="{}" AND EndsAt IS NULL;'.format(stopID, cardnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def StartTrip(cardnum, stationID):
	"""Start a trip on a given breezecard.
	cardnum (str) and stationID (str) are self-explanatory.
	Returns 1 to indicate success."""
	connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
	if PassengerInTrip():
		return "Already in trip."
	sql_findfare = 'SELECT EnterFare FROM Station WHERE StopID="{}";'.format(stationID)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql_findfare)
			fare = cursor.fetchone()[0]
	except:
		return sys.exc_info()[0]
	sql_findvalue = 'SELECT Value FROM Breezecard WHERE BreezecardNum="{}";'.format(cardnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql_findvalue)
			value = cursor.fetchone()[0]
	except:
		return sys.exc_info()[0]
	if value < fare:
		return "Insufficient funds"
	sql_update = 'INSERT INTO Trip VALUES ({}, CURRENT_TIMESTAMP, "{}", "{}", NULL);'.format(fare, cardnum, stationID)
	sql_changevalue = 'UPDATE Breezecard SET Value={} WHERE BreezecardNum="{}";'.format(value - fare, cardnum)
	try:
		with connection.cursor() as cursor:
			cursor.execute(sql_update)
			cursor.execute(sql_changevalue)
			connection.commit()
			return 1
	except:
		return sys.exc_info()[0]
	finally:
		connection.close()

def PassengerInTrip():
	"""Determine whether the user currently logged on is currently taking a trip.
	passenger_username is a global variable, so this function does not need any input parameters.
	Returns True if passenger is in a trip or False if not."""
	cardlist = [x[0] for x in ViewPassengerCards()]
	for card in cardlist:
		connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
								user = 'cs4400_Group_110',
								password = 'KAfx5IQr',
								db = 'cs4400_Group_110')
		sql = 'SELECT * FROM Trip WHERE BreezecardNum="{}" AND EndsAt IS NULL;'.format(card)
		try:
			with connection.cursor() as cursor:
				cursor.execute(sql)
				m = cursor.fetchall()
				if m:
					return True
		except:
			return sys.exc_info()[0]
	return False