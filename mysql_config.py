from getpass import getpass
import asyncio
# Define SQL configuration parameters
def get_sql_config():
    # host = input("Enter MySQL host: ")
    # db_username = input("Enter MySQL username: ")
    # db_password = getpass("Enter MySQL password: ")
    # database = input("Enter MySQL database name: ")
    
    return {
        'host': 'localhost',
        'user': 'root',
        'password': 'Inception109',
        'database': 'demodb1'
    }


# async def create_database():
#     try:
#         sql_config = get_sql_config()
#         conn = await mysql.connector.connect(**sql_config)
#         cursor = conn.cursor()
#         await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {sql_config['database']}")
#         print("Database created successfully")
#     except mysql.connector.Error as err:
#         print("Error creating database:", err)
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()
#             print("Connection closed")
