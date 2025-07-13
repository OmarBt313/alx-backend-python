import aiosqlite
import asyncio
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

# Class-based context manager for async SQLite queries
class ExecuteQuery:
    def __init__(self, database, query, params=None):
        self.database = database
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None

    async def __aenter__(self):
        try:
            self.conn = await aiosqlite.connect(self.database)
            self.cursor = await self.conn.cursor()
            # Execute the query with parameters
            await self.cursor.execute(self.query, self.params)
            # Fetch results for SELECT queries
            if self.query.strip().upper().startswith('SELECT'):
                return await self.cursor.fetchall()
            # For non-SELECT queries, return rowcount
            return self.cursor.rowcount
        except aiosqlite.Error as err:
            print(f"Database error: {err}")
            raise  # Re-raise to propagate the error

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if self.cursor:
                await self.cursor.close()
            if self.conn:
                await self.conn.commit()  # Commit changes (if any)
                await self.conn.close()
                print("Database connection closed.")
        except aiosqlite.Error as err:
            print(f"Error closing database connection: {err}")
        return False  # Propagate any exceptions

# Async function to fetch all users
@log_queries
async def async_fetch_users():
    async with ExecuteQuery(database=':memory:', query="SELECT * FROM user_data") as result:
        return result

# Async function to fetch users older than 40
@log_queries
async def async_fetch_older_users():
    async with ExecuteQuery(database=':memory:', query="SELECT * FROM user_data WHERE age > ?", params=(40,)) as result:
        return result

# Async function to set up the database and run queries concurrently
async def fetch_concurrently():
    # Initialize in-memory database
    async with aiosqlite.connect(':memory:') as conn:
        async with conn.cursor() as cursor:
            # Create user_data table
            await cursor.execute("""
                CREATE TABLE user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    age INTEGER NOT NULL
                )
            """)
            # Insert sample data
            await cursor.executemany(
                "INSERT INTO user_data (name, email, age) VALUES (?, ?, ?)",
                [
                    ('John Doe', 'john@example.com', 45),
                    ('Jane Smith', 'jane@example.com', 30),
                    ('Bob Johnson', 'bob@example.com', 50),
                    ('Alice Brown', 'alice@example.com', 25)
                ]
            )
            await conn.commit()

    # Run queries concurrently
    all_users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    return all_users, older_users

# Main execution
def main():
    try:
        # Run concurrent fetch
        all_users, older_users = asyncio.run(fetch_concurrently())

        # Print all users
        print("All user names retrieved:")
        if all_users:
            for user in all_users:
                print(user[1])  # Print name (second column: id, name, email, age)
        else:
            print("No users found.")

        # Print older users
        print("\nUser names (age > 40) retrieved:")
        if older_users:
            for user in older_users:
                print(user[1])  # Print name (second column)
        else:
            print("No users found with age > 40.")

    except aiosqlite.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()