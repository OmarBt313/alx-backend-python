import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Fightclub@1880',
        'database': 'ALX_prodev'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield int(age)
    cursor.close()
    connection.close()

def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    average = total / count if count > 0 else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    calculate_average_age()