from mysql.connector import connect, Error
from mysql_config import get_sql_config
from schema import EntFilelist

class FilelistController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def create_filelist(self, filelist, creator_username):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    # Get user ID from username
                    cursor.execute("SELECT id FROM users WHERE username = %s", (creator_username,))
                    user_id = cursor.fetchone()
                    if not user_id:
                        return {"error": "User not found"}

                    # Insert file list with creator's ID and current timestamp
                    cursor.execute("""
                        INSERT INTO filelists (name, description, created_by, created_at) 
                        VALUES (%s, %s, %s, UNIX_TIMESTAMP())""",
                        (filelist.name, filelist.description, user_id[0]))
                    
                    conn.commit()
                    print("Filelist created successfully")
                    return {"message": "Filelist created successfully"}
        except Error as e:
            print("Error creating filelist:", e)
            return {"error": "Failed to create filelist"}

    def get_filelist_info(self, filelist_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    # Retrieve file list information
                    cursor.execute("SELECT id, name, description, created_by, created_at FROM filelists WHERE id = %s", (filelist_id,))
                    filelist_data = cursor.fetchone()
                    if not filelist_data:
                        return {"error": "Filelist not found"}
                    filelist = EntFilelist(*filelist_data)

                    print("Filelist information retrieved successfully")
                    return {"filelist": filelist}
        except Error as e:
            print("Error retrieving filelist information:", e)
            return {"error": "Failed to retrieve filelist information"}

    def update_filelist(self, filelist_id, new_filelist):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE filelists 
                        SET name = %s, description = %s 
                        WHERE id = %s""",
                        (new_filelist.name, new_filelist.description, filelist_id))
                    conn.commit()
                    print("Filelist updated successfully")
                    return {"message": "Filelist updated successfully"}
        except Error as e:
            print("Error updating filelist:", e)
            return {"error": "Failed to update filelist"}

    def delete_filelist(self, filelist_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM filelists WHERE id = %s", (filelist_id,))
                    conn.commit()
                    print("Filelist deleted successfully")
                    return {"message": "Filelist deleted successfully"}
        except Error as e:
            print("Error deleting filelist:", e)
            return {"error": "Failed to delete filelist"}
