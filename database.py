import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    """Open a fresh connection to the configured MySQL database."""
    options = {
        "host": Config.DB_HOST,
        "port": Config.DB_PORT,
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "database": Config.DB_NAME,
        "connection_timeout": 10,
        "autocommit": False,
    }
    if Config.DB_SSL_CA:
        options["ssl_ca"] = Config.DB_SSL_CA
        options["ssl_verify_cert"] = True
    return mysql.connector.connect(**options)

def fetch_all(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

def fetch_one(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()
