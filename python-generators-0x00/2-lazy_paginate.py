import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the user_data table.
    Returns a list of user dictionaries.
    """
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Fightclub@1880',
        'database': 'ALX_prodev'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset)
    )
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def lazy_paginate(page_size):
    """
    Generator that yields pages of users, each page is a list of user dicts.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    for page in lazy_paginate(10):
        print(f"Page:")
        for user in page:
            print(user)