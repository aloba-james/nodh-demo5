from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from controllers import UserController, GroupController
from schema import User, Group
from sql_config import get_sql_config
import mysql.connector
import asyncio
from jwt import encode, decode


# Secret key for JWT token (replace with your own secret)
SECRET_KEY = "your_secret_key"

async def create_database():
    try:
        sql_config = get_sql_config()
        conn = await mysql.connector.connect(**sql_config)
        cursor = conn.cursor()
        await cursor.execute(f"CREATE DATABASE IF NOT EXISTS {sql_config['database']}")
        print("Database created successfully")
    except mysql.connector.Error as err:
        print("Error creating database:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed")

async def handle_request(request_handler, path, user_controller, group_controller, request_data, auth_header):
    try:
        if path.startswith('/user'):
            # Authentication check
            if not authenticate_user(auth_header):
                request_handler.send_error(401, "Unauthorized")
                return

            if path == '/user/create':
                user_data = User(username=request_data.get('username'), password=request_data.get('password'))
                response = user_controller.create_user(user_data.username, user_data.password)
            else:
                response = {"error": "Endpoint not found"}
        elif path.startswith('/group'):
            # Authentication check
            if not authenticate_user(auth_header):
                request_handler.send_error(401, "Unauthorized")
                return

            if path == '/group/create':
                group_data = Group(name=request_data.get('name'))
                response = group_controller.create_group(group_data.name)
            else:
                response = {"error": "Endpoint not found"}
        elif path == '/authenticate':
            # Call Hack for user authentication
            if hack_authenticate(request_data):
                # Generate JWT token
                jwt_token = generate_jwt_token(request_data['username'])
                response = {"jwt_token": jwt_token}
            else:
                response = {"error": "Authentication failed"}
        elif path.startswith('/dataset'):
            if path == '/dataset/create' and request_handler.command == 'POST':
                dataset_data = EntDataset(**request_data)
                response = dataset_controller.create_dataset(dataset_data.name, dataset_data.description, dataset_data.created_by)
            elif path.startswith('/dataset/read'):
                dataset_id = int(path.split('/')[-1])
                response = dataset_controller.get_dataset(dataset_id)
            elif path.startswith('/dataset/update') and request_handler.command == 'POST':
                dataset_id = int(path.split('/')[-1])
                dataset_data = EntDataset(**request_data)
                response = dataset_controller.update_dataset(dataset_id, dataset_data.name, dataset_data.description)
            elif path.startswith('/dataset/delete'):
                dataset_id = int(path.split('/')[-1])
                response = dataset_controller.delete_dataset(dataset_id)
            else:
                response = {"error": "Invalid endpoint for dataset"}
        else:
            response = {"error": "Endpoint not found"}

        request_handler.send_response(200)
        request_handler.send_header('Content-type', 'application/json')
        request_handler.end_headers()
        request_handler.wfile.write(json.dumps(response).encode('utf-8'))
    except Exception as e:
        print("Error handling request:", e)
        request_handler.send_error(500, "Internal Server Error")

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_error(400, "Bad Request: Empty request body")
                return

            auth_header = self.headers.get('Authorization')
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            asyncio.run(handle_request(self, self.path, self.user_controller, self.group_controller, request_data, auth_header))
        except json.JSONDecodeError as e:
            print("Error decoding JSON data:", e)
            self.send_error(400, "Bad Request: Invalid JSON data")
        except Exception as e:
            print("Error processing request:", e)
            self.send_error(500, "Internal Server Error")

def authenticate_user(auth_header):
    # Extract JWT token from Authorization header
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    jwt_token = auth_header.split(" ")[1]

    # Verify JWT token
    try:
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        # Additional checks can be performed here if needed
        return True
    except jwt.ExpiredSignatureError:
        print("JWT token has expired")
    except jwt.InvalidTokenError:
        print("Invalid JWT token")
    return False

def generate_jwt_token(username):
    # Generate JWT token
    payload = {"username": username}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jwt_token

def hack_authenticate(request_data):
    # Extract credentials from request data
    username = request_data.get('username')
    password = request_data.get('password')

    # Connect to the database
    try:
        sql_config = get_sql_config()
        conn = mysql.connector.connect(**sql_config)
        cursor = conn.cursor()

        # Query the database for the user's credentials
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data:
            # Compare passwords
            if user_data[1] == password:
                # Authentication successful
                return True
    except mysql.connector.Error as err:
        print("Error accessing database:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # Authentication failed
    return False

def run_server(port=8000):
    asyncio.run(create_database())

    user_controller = UserController()
    group_controller = GroupController()
    dataset_controller = DatasetController()

    RequestHandler.user_controller = user_controller
    RequestHandler.group_controller = group_controller
    RequestHandler.dataset_controller = dataset_controller

    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
