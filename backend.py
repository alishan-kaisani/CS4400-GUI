#This will be a file containing all relevant backend functions
#Functions will mostly take care of connecting to the DB

import pymysql

connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='CS4400_Group_110',
                             password='KAFx5IQr',
                             db='db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)