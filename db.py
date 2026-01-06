import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host="sql3.freesqldatabase.com",
        user="sql3813577",
        password="wbRMbUuL7A",
        database="sql3813577",
        autocommit=True

    )
