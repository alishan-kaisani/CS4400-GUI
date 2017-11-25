import pymysql
import hashlib
from random import randrange
from datetime import datetime

def VerifyLogin(self):
    """Determine whether a logon attempt is valid by querying the database.
    If the logon attempt is successful, is_admin becomes a global variable for use later on.
    is_admin is either True or False, depending on whether the user is an administrator.
    The function returns 1 if the logon attempt is successful or -1 if unsuccessful."""
	username = str(self.usernameTextEdit.toPlainText())
    password = str(self.passwordTextEdit.toPlainText())
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
    							user = 'cs4400_Group_110',
    							password = 'KAfx5IQr',
    							db = 'cs4400_Group_110')
    try:
    	with connection.cursor() as cursor:
    		# We have to somehow hash the password to make sure it's the same in the database
    		sql = 'SELECT * FROM User WHERE Username = "{}" and Password = "{}";'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest())
    		cursor.execute(sql)
            m = cursor.fetchall()
            global is_admin
            is_admin = bool(m[0][2]) if m else None
            return 1 if m else -1 # 1 if successful, -1 if unsuccessful
    except:
    	print("This should have worked. Blame Joel")
    finally:
    	connection.close()
    	# print("Finished login query") #For testing purposes only

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

def CreateNewUser(username, email, password, cardnumber=None):
    """Adds a new user to the database; inserts tuples into User, Passenger, and Breezecard tables.
    Returns 1 if the operation is successful, otherwise an exception is raised."""
    if cardnumber is None:
        cardnumber = GenerateNewCardNumber()
    assert len(str(cardnumber)) == 16, "Card number must be 16 digits"
    sql = 'INSERT INTO User VALUES ("{}", "{}", false);'.format(username, hashlib.md5(password.encode('utf-8')).hexdigest()) #New users are always passengers, not admins
    sql2 = 'INSERT INTO Passenger VALUES ("{}", "{}");'.format(username, email)
    sql3 = 'INSERT INTO Breezecard VALUES ("{}", 0.00, "{}");'.format(cardnumber, username)
    sql_query = 'SELECT * FROM Breezecard WHERE Breezecard="{}";'.format(cardnumber)
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
        print("Something went wrong. Blame Joel")
    finally:
        connection.close()

def CreateNewUserWrapper(existing_card, username, email, password, *args):
    """Calls the CreateNewUser function depending on whether the new user is using an existing Breeze Card or wishes to generae a new one.
    existing_card is a boolean parameter that determines whether the new user already has a breezecard.
    username, email, and password have the same meaning as they do in CreateNewUser.
    *args allows for the optional parameter (Breeze Card number) to be called when existing_card == True.
    Returns 1 if successful, otherwise an exception is raised."""
    if existing_card == False:
        CreateNewUser(username, email, password)
    else:
        CreateNewUser(username, email, password, args[0])
    # The CreateNewUser function will return 1, so we do not need to include a return statement in this function

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
        print("Something went wrong. Blame Joel.")
    finally:
        connection.close()

def PrettifyViewStations(orderBy='Name'):
    """Makes the station listing from the ViewStations() function usable, since each station's fare will no longer be a Decimal object.
    orderBy (str) takes the same values and has the same meaning as in the ViewStations() function.
    Returns a list of several tuples where the Decimal object is replaced by a floating point number (otherwise an exception would have been raised)."""
    listing = ViewStations(orderBy)
    newlisting = []
    for tup in listing:
        newlisting.append((tup[0], tup[1], round(float(tup[2]), 2), tup[3]))
    return newlisting

def ViewSingleStation(stopID):
    """Returns a tuple with information on a single station.
    stopID (str) is self-explanatory and the primary key of the database."""
    connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                                user = 'cs4400_Group_110',
                                password = 'KAfx5IQr',
                                db = 'cs4400_Group_110')
    sql = 'SELECT Name, StopID, EnterFare, ClosedStatus FROM Station WHERE stopID="{}";'.format(stopID)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            m = cursor.fetchone()
            return (m[0], m[1], float(m[2]), m[3]) if m else ()
    except:
        print("Something went wrong. Blame Joel.")
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
        print("Someting went wrong. Blame Joel.")
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
    sql = 'INSERT INTO Station VALUES ("{}", "{}", {}, {}, false);'.format(stopID, stationName, entryFare, closedStatus)
    if args:
        sql2 = 'INSERT INTO BusStationIntersection VALUES ("{}", "{}");'.format(stopID, args[0])
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
            if args:
                cursor.execute(sql2)
                connection.commit()
            return 1
    except:
        print("Someting went wrong. Blame Joel.")
    finally:
        connection.close()

def CreateStationWrapper(isTrain, stationName, stopID, entryFare, closedStatus, *args):
    """Wrapper function for creating new station.
    isTrain (bool) determines whether the new station is a train station.
    *args creates variable args (tuple) with 0 or 1 elements (that element, if it exists, is a string of the nearest intersection for bus stations only).
    Parameters stationName (str), stopID (str), entryFare (float), and closedStatus (bool or int) have the same meaning as before."""
    if isTrain:
        CreateTrainStation(stationName, stopID, entryFare, closedStatus)
    elif not args:
        CreateBusStation(stationName, stopID, entryFare, closedStatus)
    else:
        CreateBusStation(stationName, stopID, entryFare, closedStatus, args[0])

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
        print("Something went wrong. Blame Joel.")
    finally:
        connection.close()

def PrettifyViewSuspendedCards():
    """Returns a list of tuples of rows from the ViewSuspendedCards() function query that is manageable.
    The datetime.datetime objects returned from ViewSuspendedCards are now strings that are manageable."""
    listing = ViewSuspendedCards()
    newlisting = []
    for tup in listing:
        newlisting.append((tup[0], tup[1], str(tup[2]), tup[3]))
    return newlisting

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
        print("Something went wrong. Blame Joel.")
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
        print("Something went wrong. Blame Joel.")
    finally:
        connection.close()

