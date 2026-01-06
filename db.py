import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="NarkuUser",
        password="V0113yb@11ru135",
        database="Collection",
        autocommit=True
    )