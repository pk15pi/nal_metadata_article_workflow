import os
import requests
import mysql.connector
from mysql.connector import Error
import json
import tomli

class HandleClient:
    """
    Client for minting PIDs and Handles, and checking their existence in the database.
    Handles connections to PID and Handle MySQL databases and interacts with the Handle API.
    """

    def __init__(self, testing_mode=False):
        """
        Initialize the HandleClient with environment variables for database credentials and API endpoint.
        Establishes connections to PID and Handle databases.
        """

        self.testing_mode = testing_mode # If testing_mode, don't connect to databases or handle server

        # PID DB credentials
        self.pid_db_name = os.getenv("PID_DB_NAME")
        self.pid_db_user = os.getenv("PID_DB_USER")
        self.pid_db_password = os.getenv("PID_DB_PASSWORD")
        self.pid_db_host = os.getenv("PID_DB_HOST")
        self.pid_db_port = os.getenv("PID_DB_PORT")

        # Handle DB credentials
        self.handle_db_name = os.getenv("HANDLE_DB_NAME")
        self.handle_db_user = os.getenv("HANDLE_DB_USER")
        self.handle_db_password = os.getenv("HANDLE_DB_PASSWORD")
        self.handle_db_host = os.getenv("HANDLE_DB_HOST")
        self.handle_db_port = os.getenv("HANDLE_DB_PORT")

        # Handle API endpoint
        self.mint_handle_api = os.getenv("MINT_HANDLE_API_URL", "https://199.133.202.73:8000/api/handles/10113/{0}")
        if not self.testing_mode:
            self.pid_db = self.connect_pid_db()
            self.handle_db = self.connect_handle_db()

        self.base_path = os.path.dirname(os.path.abspath(__file__))

        self.headers_path = os.getenv("HANDLE_API_HEADERS")
        if self.headers_path is None:
            raise ValueError("HANDLE_API_HEADERS environment variable is not set")

    def connect_pid_db(self):
        """
        Establish a connection to the PID MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection or None: Database connection object or None if connection fails.
        """
        try:
            connection = mysql.connector.connect(
                host=self.pid_db_host,
                user=self.pid_db_user,
                password=self.pid_db_password,
                database=self.pid_db_name,
                port=self.pid_db_port,
                charset="utf8mb4",
                collation="utf8mb4_general_ci"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to PID MySQL: {e}")
        return None

    def connect_handle_db(self):
        """
        Establish a connection to the Handle MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection or None: Database connection object or None if connection fails.
        """
        try:
            connection = mysql.connector.connect(
                host=self.handle_db_host,
                user=self.handle_db_user,
                password=self.handle_db_password,
                database=self.handle_db_name,
                port=self.handle_db_port,
                charset="utf8mb4",
                collation="utf8mb4_general_ci"
            )
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error while connecting to Handle MySQL: {e}")
        return None

    def mint_pid(self) -> int:
        """
        Mint a new PID by requesting the next value from the PID database.

        Returns:
            int or 0: The next available PID, or 0 if not available.
        """
        if self.testing_mode:
            return 0
        pid_db_cursor = self.pid_db.cursor()
        pid_db_cursor.execute("SELECT nextval(pid) from pid")
        row = pid_db_cursor.fetchone()
        next_pid = row[0] if row else 0
        return next_pid

    def check_handle_exists(self, handle):
        """
        Check if a handle already exists in the Handle database.

        ** It would be better to check by the Handle URL. **

        Args:
            handle (str): The handle to check.

        Returns:
            bool: True if the handle exists, False otherwise.
        """
        if self.testing_mode:
            return False
        handle_db_cursor = self.handle_db.cursor()
        handle_db_cursor.execute("SELECT * FROM handles WHERE handle = %s", (handle,))
        result = handle_db_cursor.fetchall()
        return len(result) > 0

    def check_landing_page_exists(self, landing_page_url):
        """
        Check if a landing page URL is already associated with a handle in the Handle database.

        Args:
            landing_page_url (str): The landing page URL to check.

        Returns:
            bool: True if the landing page URL exists, False otherwise.
        """
        if self.testing_mode:
            return False
        handle_db_cursor = self.handle_db.cursor()
        handle_db_cursor.execute("SELECT * FROM handles WHERE data = %s", (landing_page_url,))
        result = handle_db_cursor.fetchall()

        return len(result) > 0

    def create_handle(self, pid, landing_page_url):
        """
        Mint a new handle using the given PID and landing page URL via the Handle API.

        Args:
            pid (str): The PID to use in the handle.
            landing_page_url (str): The URL to associate with the handle.

        Returns:
            str or None: The minted handle string, or None if minting failed.
        """

        with open(self.headers_path, 'r') as f:
            headers = json.load(f)
        handle_prefix = "10113"
        handle = f"{handle_prefix}/{pid}"
        json_data = {
            "handle": handle,
            "values": [
                {
                    "index": 1,
                    "type": "URL",
                    "data": {
                        "format": "string",
                        "value": landing_page_url
                    }
                },
                {
                    "index": 100,
                    "type": "HS_ADMIN",
                    "data": {
                        "format": "admin",
                        "value": {
                            "handle": "0.NA/10113",
                            "index": 300,
                            "permissions": "111111111111",
                            "legacyByteLength": True
                        }
                    }
                }
            ]
        }

        try:
            url = self.mint_handle_api.format(pid)
            print("Making request to url: ", url)
            res = requests.put(url, json=json_data, headers=headers, verify=False) # May take up to 40 minutes
            res.raise_for_status()
            return handle
        except Exception as err:
            print(f"Error minting handle: {err}")
            return None
