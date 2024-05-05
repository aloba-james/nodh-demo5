from mysql.connector import connect, Error
from mysql_config import get_sql_config
from schema import EntMetadata


class MetadataController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def create_metadata(self, name, value):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS metadata (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            value TEXT
                        )
                    """)
                    cursor.execute(
                        "INSERT INTO metadata (name, value) VALUES (%s, %s)", (name, value))
                    conn.commit()
                    print("Metadata created successfully")
                    return {"message": "Metadata created successfully"}
        except Error as e:
            print("Error creating metadata:", e)
            return {"error": "Failed to create metadata"}

    def get_metadata(self, offset=0, limit=10):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, name, description, created_by, created_at FROM metadata LIMIT %s OFFSET %s", (limit, offset))
                    metadata_data = cursor.fetchall()
                    metadata = [EntMetadata(*item) for item in metadata_data]
                    print("Metadata retrieved successfully")
                    return {"metadata": metadata}
        except Error as e:
            print("Error retrieving metadata:", e)
            return {"error": "Failed to retrieve metadata"}

    def get_metadata_by_id(self, metadata_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, name, description, created_by, created_at FROM metadata WHERE id = %s", (metadata_id,))
                    metadata_data = cursor.fetchone()
                    if metadata_data:
                        metadata = EntMetadata(*metadata_data)
                        print("Metadata retrieved successfully")
                        return {"metadata": metadata}
                    else:
                        return {"error": "Metadata not found"}
        except Error as e:
            print("Error retrieving metadata:", e)
            return {"error": "Failed to retrieve metadata"}

    def update_metadata(self, metadata_id, name, value):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE metadata SET name = %s, value = %s WHERE id = %s", (name, value, metadata_id))
                    conn.commit()
                    print("Metadata updated successfully")
                    return {"message": "Metadata updated successfully"}
        except Error as e:
            print("Error updating metadata:", e)
            return {"error": "Failed to update metadata"}

    def delete_metadata(self, metadata_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM metadata WHERE id = %s", (metadata_id,))
                    conn.commit()
                    print("Metadata deleted successfully")
                    return {"message": "Metadata deleted successfully"}
        except Error as e:
            print("Error deleting metadata:", e)
            return {"error": "Failed to delete metadata"}
