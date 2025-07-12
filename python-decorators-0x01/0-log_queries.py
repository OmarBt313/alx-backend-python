# import mysql.connector
# import functools
# from getpass import getpass
# #### decorator to log SQL queries

# def log_queries(func):
#     def wrapper(*args, **kwargs):
#         query = args[0] if args else kwargs.get('query', '')
#         print(f"Executing query: {query}")
#         return func(*args, **kwargs)
#     return wrapper

# @log_queries
# def fetch_all_users(query):
#     conn = mysql.connector.connect(
#         host='localhost',         # Change if your MySQL server is remote
#         user=username,     # Use your MySQL username
#         password=password, # Use your MySQL password
#         database='alx_prodev'  # Use your database name
#     )
#     cursor = conn.cursor()
#     cursor.execute(query)
#     results = cursor.fetchall()
#     conn.close()
#     return results

# #### Prompt for username and password
# username = input("Enter MySQL username: ")
# password = getpass("Enter MySQL password: ")

# #### fetch users while logging the query
# users = fetch_all_users("SELECT * FROM user_data")
# print(f'{users}')

import mysql.connector
from getpass import getpass
import functools
from datetime import datetime

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get('query', '')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query, username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user=username,
            password=password,
            database='alx_prodev'
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Fetch users while logging the query
        users = fetch_all_users("SELECT * FROM user_data", username, password)
        
        if users:
            print("Users retrieved:")
            for user in users:
                print(f"User: {user}")
        else:
            print("No users found or error occurred.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()