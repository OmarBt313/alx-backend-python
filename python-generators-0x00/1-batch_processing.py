import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    Each batch is a list of dictionaries.
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
    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25.
    Prints the filtered users.
    """
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if int(user['age']) > 25]
        for user in filtered:
            print(user)

if __name__ == "__main__":
    batch_processing(10)

#return 