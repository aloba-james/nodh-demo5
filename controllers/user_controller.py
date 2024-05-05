from mysql.connector import connect, Error  
from mysql_config import get_sql_config



class UserController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def create_user(self, username, password):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(255) UNIQUE,
                            password VARCHAR(255)
                        )
                    """)
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    print("User created successfully")
                    return {"message": "User created successfully"}
        except Error as e:
            print("Error creating user:", e)
            return {"error": "Failed to create user"}
