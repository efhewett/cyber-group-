import mysql.connector
from mysql.connector import Error
import config


def create_connection():
    """Create a database connection using the configuration from config.py."""
    try:
        connection = mysql.connector.connect(
            host=config.HOST,
            user=config.USER,
            password=config.PASSWORD,
            database=config.DATABASE
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """Close the database connection."""
    if connection:
        connection.close()

def execute_query(query, params=None):
    """Execute a SQL query and return the result or True/False for success/failure."""
    connection = create_connection()
    if connection is None:
        return False
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        if cursor.lastrowid:
            return cursor.lastrowid
        else:
            return True
    except Error as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        close_connection(connection)

def fetch_data(query, params=None):
    """Fetch data from the database using a select query."""
    connection = create_connection()
    if connection is None:
        return []
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error fetching data: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        close_connection(connection)

def insert_data(table, data):
    """Insert data into a specified table."""
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    values = tuple(data.values())

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    return execute_query(query, values)
