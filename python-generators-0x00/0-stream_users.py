import mysql.connector

def stream_users():
    """
    Generator that yields rows from the user_data table one by one.
    """
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Fightclub@1880',
        'database': 'ALX_prodev'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    connection.close()

if __name__ == "__main__":
    for user in stream_users():
        print(user)