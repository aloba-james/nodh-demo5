from mysql.connector import connect, Error
from schema import User, Group
from sql_config import get_sql_config

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

class DatasetController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def create_dataset(self, name, description, created_by):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS datasets (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            description TEXT,
                            created_by INT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (created_by) REFERENCES users(id)
                        )
                    """)
                    cursor.execute("INSERT INTO datasets (name, description, created_by) VALUES (%s, %s, %s)", (name, description, created_by))
                    conn.commit()
                    print("Dataset created successfully")
                    return {"message": "Dataset created successfully"}
        except Error as e:
            print("Error creating dataset:", e)
            return {"error": "Failed to create dataset"}

    def get_dataset(self, dataset_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM datasets WHERE id = %s", (dataset_id,))
                    dataset = cursor.fetchone()
                    if dataset:
                        dataset_dict = {
                            "id": dataset[0],
                            "name": dataset[1],
                            "description": dataset[2],
                            "created_by": dataset[3],
                            "created_at": dataset[4].timestamp()
                        }
                        return dataset_dict
                    else:
                        return {"error": "Dataset not found"}
        except Error as e:
            print("Error retrieving dataset:", e)
            return {"error": "Failed to retrieve dataset"}

    def update_dataset(self, dataset_id, name, description):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE datasets SET name = %s, description = %s WHERE id = %s", (name, description, dataset_id))
                    conn.commit()
                    print("Dataset updated successfully")
                    return {"message": "Dataset updated successfully"}
        except Error as e:
            print("Error updating dataset:", e)
            return {"error": "Failed to update dataset"}

    def delete_dataset(self, dataset_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM datasets WHERE id = %s", (dataset_id,))
                    conn.commit()
                    print("Dataset deleted successfully")
                    return {"message": "Dataset deleted successfully"}
        except Error as e:
            print("Error deleting dataset:", e)
            return {"error": "Failed to delete dataset"}