import os
import mysql.connector
from mysql.connector import Error


# connect to the pid database
def connect_pid_db():
    # Fetch database credentials from environment variables
    db_name = os.getenv("PID_DB_NAME")
    db_user = os.getenv("PID_DB_USER")
    db_password = os.getenv("PID_DB_PASSWORD")
    db_host = os.getenv("PID_DB_HOST")
    db_port = os.getenv("PID_DB_PORT")

    try:
        # Establish the database connection
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port
        )

        # if connection is successful
        if connection.is_connected():
            return connection
        else:
            return None

    # return None if connection is not successful
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None



def pid_minter(citation_object):
    result = []
    pid_db_connection = connect_pid_db()

    # if pid_db_connection and article_db_connection:
    if pid_db_connection:
        pid_db = pid_db_connection.cursor()

        # generate the new PID
        pid_db.execute("SELECT * AUTO_INCREMENT FROM PID")
        next_pid = pid_db.fetchone()
        next_pid = next_pid[0] 

        if citation_object['type'] is not 'journal-article':
            result =[citation_object , "Non Article", None]

        else:
            if citation_object['local']['identifier']['pid']:
                result = [citation_object , "PID Already Assinged", None]
            else:
                citation_object['local']['identifier']['pid'] = next_pid
                result = [citation_object , "PID Assinged", next_pid]

    else:
        result = [citation_object , "Database connection error occured", None]

    if pid_db_connection:
        pid_db_connection.close()
    
    return result

