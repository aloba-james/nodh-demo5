from mysql.connector import connect, Error
from mysql_config import get_sql_config
from schema import EntDataset

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

    def get_datasets(self, offset=0, limit=10):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name, description, created_by, created_at FROM datasets LIMIT %s OFFSET %s", (limit, offset))
                    datasets_data = cursor.fetchall()
                    datasets = [EntDataset(*dataset_data) for dataset_data in datasets_data]
                    print("Datasets retrieved successfully")
                    return {"datasets": datasets}
        except Error as e:
            print("Error retrieving datasets:", e)
            return {"error": "Failed to retrieve datasets"}

    def get_dataset_by_id(self, dataset_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, name, description, created_by, created_at FROM datasets WHERE id = %s", (dataset_id,))
                    dataset_data = cursor.fetchone()
                    if dataset_data:
                        dataset = EntDataset(*dataset_data)
                        print("Dataset retrieved successfully")
                        return {"dataset": dataset}
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