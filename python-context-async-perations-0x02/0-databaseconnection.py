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

# Class-based context manager for database connections
class DatabaseConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            return self.conn, self.cursor
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            raise  # Re-raise the exception to propagate it

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn and self.conn.is_connected():
                self.conn.commit()  # Commit any changes
                self.conn.close()
                print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing database connection: {err}")
        return False  # Propagate any exceptions

# Function to fetch all users
@log_queries
def fetch_users(conn, cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Use context manager to fetch users
        with DatabaseConnection(host='localhost', user=username, password=password, database='alx_prodev') as (conn, cursor):
            users = fetch_users(conn, cursor, query="SELECT * FROM user_data")
            if users:
                print("User names retrieved:")
                for user in users:
                    print(user[1])  # Print only the name (second column, assuming id, name, email)
            else:
                print("No users found or error occurred.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()