import mysql.connector
from getpass import getpass
import functools
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
                    conn.commit()  # Commit any changes (if applicable)
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

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Apply the decorator with credentials
        @with_db_connection(username, password)
        @log_queries
        def get_all_users(conn, cursor):
            query = "SELECT name FROM user_data"
            cursor.execute(query)
            return cursor.fetchall()

        # Fetch all users
        users = get_all_users()
        if users:
            print("User names retrieved:")
            for user in users:
                print(user[0])  # Print only the name (first column)
        else:
            print("No users found or error occurred.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()