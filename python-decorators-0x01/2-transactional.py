# import mysql.connector
# import functools
# from getpass import getpass

# """your code goes here"""
# def transactional(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         conn = args[0]  # Assuming the first argument is the connection
#         try:
#             result = func(*args, **kwargs)
#             conn.commit()  # Commit the transaction
#             return result
#         except Exception as e:
#             conn.rollback()  # Rollback on error
#             print(f"Transaction failed: {e}")
#             raise
#     return wrapper

# def with_db_connection(username, password):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 conn = mysql.connector.connect(
#                     host='localhost',
#                     user=username,
#                     password=password,
#                     database='alx_prodev'
#                 )
#                 cursor = conn.cursor()
#                 try:
#                     result = func(conn, cursor, *args, **kwargs)
#                     conn.commit()  # Commit any changes (if applicable)
#                     return result
#                 finally:
#                     cursor.close()
#                     if conn.is_connected():
#                         conn.close()
#                         print("Database connection closed.")
#             except mysql.connector.Error as err:
#                 print(f"Database error: {err}")
#                 return None
#         return wrapper
#     return decorator

# username = input("Enter MySQL username: ")
# password = getpass("Enter MySQL password: ")
# @with_db_connection(username, password)
# @transactional
# def update_user_email(conn, user_id, new_email):
#     cursor = conn.cursor()
#     cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
#     #### Update user's email with automatic transaction handling 

# update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

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

# Decorator to ensure transactional behavior
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, cursor, *args, **kwargs):
        try:
            # Ensure autocommit is disabled to start a transaction
            conn.autocommit = False
            # Execute the function
            result = func(conn, cursor, *args, **kwargs)
            # Commit the transaction if no errors
            conn.commit()
            return result
        except Exception as e:
            # Roll back the transaction on any error
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            return None
        finally:
            # Reset autocommit to default (optional, for safety)
            conn.autocommit = True
    return wrapper

# Main execution
def main():
    try:
        # Prompt for username and password
        username = input("Enter MySQL username: ")
        password = getpass("Enter MySQL password: ")

        # Function to update user email by ID
        @with_db_connection(username, password)
        @log_queries
        @transactional
        def update_user_email(conn, cursor, user_id, new_email):
            query = "UPDATE user_data SET email = %s WHERE id = %s"
            cursor.execute(query, (new_email, user_id))
            return cursor.rowcount  # Return number of affected rows

        # Update user's email with automatic transaction handling
        affected_rows = update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        if affected_rows is not None and affected_rows > 0:
            print(f"Updated {affected_rows} user(s) with ID 1.")
        else:
            print("No user found with ID 1 or error occurred.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()