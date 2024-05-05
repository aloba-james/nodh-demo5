from mysql.connector import connect, Error
from mysql_config import get_sql_config


class GroupController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def create_group(self, name):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS groups (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255) UNIQUE
                        )
                    """)
                    cursor.execute("INSERT INTO groups (name) VALUES (%s)", (name,))
                    conn.commit()
                    print("Group created successfully")
                    return {"message": "Group created successfully"}
        except Error as e:
            print("Error creating group:", e)
            return {"error": "Failed to create group"}
