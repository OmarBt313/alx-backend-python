import mysql.connector
from getpass import getpass
import functools
from datetime import datetime

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = args[0] if len(args) > 0 else kwargs.get('query', '')  # Query is the first arg
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Class-based context manager for executing queries
class ExecuteQuery:
    def __init__(self, host, user, password, database, query, params=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.query = query
        self.params = params if params is not None else ()
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
            # Execute the query with parameters
            self.cursor.execute(self.query, self.params)
            # Fetch results for SELECT queries
            if self.query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            # For non-SELECT queries, return rowcount
            return self.cursor.rowcount
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            raise  # Re-raise to propagate the error

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn and self.conn.is_connected():
                self.conn.commit()  # Commit changes (if any)
                self.conn.close()
                print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing database connection: {err}")
        return False  # Propagate any exceptions

# Function to execute query with logging
@log_queries
def execute_query(query, params=None):
    username = input("Enter MySQL username: ")
    password = getpass("Enter MySQL password: ")
    with ExecuteQuery(
        host='localhost',
        user=username,
        password=password,
        database='alx_prodev',
        query=query,
        params=params
    ) as result:
        return result

# Main execution
def main():
    try:
        # Execute the query with parameter
        query = "SELECT * FROM user_data WHERE age > %s"
        users = execute_query(query, params=(25,))
        if users:
            print("User names retrieved:")
            for user in users:
                print(user[1])  # Print only the name (second column, assuming id, name, email, age)
        else:
            print("No users found or error occurred.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()