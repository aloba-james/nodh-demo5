from mysql.connector import connect, Error
from mysql_config import get_sql_config
from schema import EntAnnotation

class AnnotationController:
    def __init__(self):
        self.sql_config = get_sql_config()

    def store_annotation_result(self, annotation_data):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO annotations (recording_id, start_time, end_time, description, created_by, created_at) 
                        VALUES (%s, %s, %s, %s, %s, UNIX_TIMESTAMP())""",
                        (annotation_data.recording_id, annotation_data.start_time,
                         annotation_data.end_time, annotation_data.description, 
                         annotation_data.created_by))
                    
                    conn.commit()
                    print("Annotation result stored successfully")
                    return {"message": "Annotation result stored successfully"}
        except Error as e:
            print("Error storing annotation result:", e)
            return {"error": "Failed to store annotation result"}

    def retrieve_annotation_data(self, recording_id):
        try:
            with connect(**self.sql_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM annotations WHERE recording_id = %s", (recording_id,))
                    annotation_data = cursor.fetchall()
                    if not annotation_data:
                        return {"error": "No annotation data found for recording"}
                    print("Annotation data retrieved successfully")
                    return {"annotation_data": annotation_data}
        except Error as e:
            print("Error retrieving annotation data:", e)
            return {"error": "Failed to retrieve annotation data"}
