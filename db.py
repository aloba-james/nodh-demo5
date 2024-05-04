from mysql.connector import connect, Error 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Inception109',
}

def create_database():
    try:
        with connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE demodb")
        print("Database created successfully")
    except Error as e:
        print("Error creating database: ", e)

if __name__ == '__main__':
    create_database()