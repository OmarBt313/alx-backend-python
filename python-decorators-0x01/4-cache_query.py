import mysql.connector
from getpass import getpass
import functools
import time
from datetime import datetime

# Cache dictionary to store query results
query_cache = {}

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

# Decorator to cache query results based on query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query string (third arg or from kwargs)
        query = args[2] if len(args) > 2 else kwargs.get('query', '')
        # Check if query result is in cache
        if query in query_cache:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Using cached result for query: {query}")
            return query_cache[query]
        # Execute query if not cached
        result = func(*args, **kwargs)
        # Cache the result if query was successful
        if result is not None:
            query_cache[query] = result
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Cached result for query: {query}")
        return result
    return wrapper

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Function to fetch users with caching
        @with_db_connection(username, password)
        @log_queries
        @cache_query
        def fetch_users_with_cache(conn, cursor, query):
            cursor.execute(query)
            return cursor.fetchall()

        # First call will execute and cache the result
        print("First call:")
        users = fetch_users_with_cache(query="SELECT * FROM user_data")
        if users:
            print("User names retrieved:")
            for user in users:
                print(user[1])  # Print only the name (second column, assuming id, name, email)
        else:
            print("No users found or error occurred.")

        # Second call will use the cached result
        print("\nSecond call:")
        users_again = fetch_users_with_cache(query="SELECT * FROM user_data")
        if users_again:
            print("User names retrieved:")
            for user in users_again:
                print(user[1])  # Print only the name
        else:
            print("No users found or error occurred.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()