import os
import mysql.connector
from mysql.connector import Error
import pickle

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



def pid_minter():
    article_db_connection = connect_article_db()
    pid_db_connection = connect_pid_db()

    if article_db_connection and pid_db_connection:
        article_db = article_db_connection.cursor(dictionary=True)
        pid_db = pid_db_connection.cursor()

        # Update the article record with the new PID
        article_result_query = "SELECT * FROM model_article where last_step=6" 
        article_db.execute(article_result_query)
        article_records = article_db.fetchall()

        unpickle_content = None

        # iterate over the article records and generate / update PIDs
        for x in article_records:
            # generate the new PID
            pid_db.execute("SELECT * AUTO_INCREMENT FROM PID")
            next_pid = pid_db.fetchone()
            next_pid = next_pid[0]

            citation_object_path = x['citation_pickle'] 

            if x['pid']:
                print('PID Already Assinged')
            else:
                try:
                    with open(citation_object_path, 'rb') as file:
                        unpickle_content = pickle.load(file)
                except Exception as e:
                    print('Error loading pickle file', e)
                    continue

                unpickle_content = unpickle_content.__dict__
                if x['type_of_recod'] == 'journal-article':
                    query = 'UPDATE model_article SET pid = %s WHERE ID=%s'
                    article_db.execute(query, next_pid, x['ID'])
                    article_db.commit()

    # close the database connections
    if article_db_connection:
        article_db_connection.close()
    if pid_db_connection:
        pid_db_connection.close()
    
    return None

