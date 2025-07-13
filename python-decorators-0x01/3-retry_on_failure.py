import mysql.connector
from getpass import getpass
import functools
import time
from datetime import datetime

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[2] if len(args) > 2 else kwargs.get('query', '')  # Query is the third arg (after conn, cursor)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Decorator to handle database connection
def with_db_connection(username, password):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user=username,
                    password=password,
                    database='alx_prodev'
                )
                cursor = conn.cursor()
                try:
                    result = func(conn, cursor, *args, **kwargs)
                    return result
                finally:
                    cursor.close()
                    if conn.is_connected():
                        conn.close()
                        print("Database connection closed.")
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                return None
        return wrapper
    return decorator

# Decorator to retry function on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed with error: {e}")
                    if attempt == retries:
                        print(f"All {retries} retry attempts failed.")
                        return None
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Function to fetch all users with retry
        @with_db_connection(username, password)
        @log_queries
        @retry_on_failure(retries=3, delay=1)
        def fetch_users_with_retry(conn, cursor):
            query = "SELECT * FROM user_data"  # Updated to user_data
            cursor.execute(query)
            return cursor.fetchall()

        # Attempt to fetch users with automatic retry on failure
        users = fetch_users_with_retry()
        if users:
            print("User names retrieved:")
            for user in users:
                print(user[1])  # Print only the name (second column, assuming id, name, email)
        else:
            print("No users found or error occurred.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()