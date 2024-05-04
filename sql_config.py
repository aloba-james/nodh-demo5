from getpass import getpass

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
