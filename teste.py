import mysql.connector 
from mysql.connector import errorcode

try:
    db_connection = mysql.connector.connect(host='186.209.139.200', user='jacsoncom', password='Bancodedados@2', database='jacsonco_tickets')
    print("Database connection made!")

    cursor = db_connection.cursor()
    cursor.execute("select * from tickets")
    for r in cursor:
        print(r)

except mysql.connector.Error as error:
    if error.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database doesn't exist")
    elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("User name or password is wrong")
    else:
	    print(error)
else:
	db_connection.close()