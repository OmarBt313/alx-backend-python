import mysql.connector
import functools
from getpass import getpass
#### decorator to log SQL queries

def log_queries(func):
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get('query', '')
        print(f"Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = mysql.connector.connect(
        host='localhost',         # Change if your MySQL server is remote
        user=username,     # Use your MySQL username
        password=password, # Use your MySQL password
        database='alx_prodev'  # Use your database name
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### Prompt for username and password
username = input("Enter MySQL username: ")
password = getpass("Enter MySQL password: ")

#### fetch users while logging the query
users = fetch_all_users("SELECT * FROM user_data")
print(f'{users}')