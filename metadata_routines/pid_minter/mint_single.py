import os
import mysql.connector
from mysql.connector import Error


# connect to the article database
def connect_article_db():
    # Fetch database credentials from environment variables
    db_name = os.getenv("ARTICLE_DB_NAME")
    db_user = os.getenv("ARTICLE_DB_USER")
    db_password = os.getenv("ARTICLE_DB_PASSWORD")
    db_host = os.getenv("ARTICLE_DB_HOST")
    db_port = os.getenv("ARTICLE_DB_PORT")

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
            print("Successfully connected to the database")
            return connection
        else:
            return None
        
    # return none if connection is not successful
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None



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



def pid_minter(citation_object, article):
    article_db_connection = connect_article_db()
    pid_db_connection = connect_pid_db()

    if pid_db_connection and article_db_connection:
        article_db = article_db_connection.cursor(dictionary=True)
        pid_db = pid_db_connection.cursor()

        # generate the new PID
        pid_db.execute("SELECT * AUTO_INCREMENT FROM PID")
        next_pid = pid_db.fetchone()
        next_pid = next_pid[0] 

        if article['pid']:
            return citation_object , "PID Already Assinged"
        else:
            if article['type_of_recod'] == 'journal-article':
                article['pid'] = next_pid
                query = 'UPDATE model_article SET pid = %s WHERE ID=%s'
                article_db.execute(query, next_pid, article['ID'])
                article_db.commit()
                return citation_object , "New PID Assinged"
            else:
                return citation_object , "Article is not a journal-article"

    # close the database connections
    if article_db_connection:
        article_db_connection.close()
    if pid_db_connection:
        pid_db_connection.close()
    
    return citation_object , "Database connection error occured"

