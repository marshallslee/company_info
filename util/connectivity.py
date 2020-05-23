import mysql.connector
from mysql.connector import Error
from config.config import db

connection = mysql.connector.connect(host=db['host'],
                                     database=db['database'],
                                     user=db['user'],
                                     password=db['password'])
cursor = connection.cursor()


def check_db_connectivity():
    try:
        if connection.is_connected():
            db_info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_info)
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return True
        else:
            return False

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    connectivity = check_db_connectivity()
    print(connectivity)
