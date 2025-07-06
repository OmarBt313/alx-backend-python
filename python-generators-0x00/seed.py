import mysql.connector
import csv
import uuid

# --- Database Connection Details ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Fightclub@1880'
}

# --- Path to your CSV file ---
CSV_FILE_PATH = r"G:\User_Omar\documents\ALX\git_projects2\alx-backend-python\python-generators-0x00\user_data.csv"

def setup_database():
    """
    Connects to MySQL, creates the database and table,
    and populates it from a CSV file.
    """
    db_connection = None
    try:
        # --- 1. Connect to MySQL Server ---
        print("Connecting to MySQL Server...")
        db_connection = mysql.connector.connect(**DB_CONFIG)
        cursor = db_connection.cursor()
        print("✅ Connection successful!")

        # --- 2. Create the Database ---
        print("Creating database ALX_prodev...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.execute("USE ALX_prodev")
        print("✅ Database created and selected.")

        # --- 3. Create the Table ---
        print("Creating table user_data...")
        create_table_query = """
        DROP TABLE IF EXISTS user_data;
        CREATE TABLE user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            INDEX(user_id)
        )
        """
        for statement in create_table_query.strip().split(';'):
            if statement.strip():
                cursor.execute(statement)
        print("✅ Table 'user_data' created.")

        # --- 4. Populate the Table from CSV ---
        print(f"Populating data from {CSV_FILE_PATH}...")

        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"

        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            print(f"CSV Headers found: {csv_reader.fieldnames}")  # Debugging line

            data_to_insert = [
                (str(uuid.uuid4()), row['name'], row['email'], row['age'])
                for row in csv_reader
            ]

        if data_to_insert:
            cursor.executemany(insert_query, data_to_insert)
            db_connection.commit()
            print(f"✅ Successfully inserted {cursor.rowcount} rows.")
        else:
            print("CSV file is empty or could not be read.")

    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    except KeyError as e:
        print(f"❌ KeyError: A column name {e} was not found in the CSV header. Please check your file.")
    finally:
        if db_connection and db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    setup_database()