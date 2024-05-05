from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from controllers import *
from schema import *
from mysql_config import get_sql_config, create_database
import mysql.connector
import asyncio
import jwt


# Secret key for JWT token (replace with your own secret)
SECRET_KEY = "secret_key_demo5"


class RequestHandler(BaseHTTPRequestHandler):
    user_controller = UserController()
    group_controller = GroupController()
    dataset_controller = DatasetController()
    filelist_controller = FilelistController()

    async def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_error(400, "Bad Request: Empty request body")
                return

            auth_header = self.headers.get('Authorization')
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            # user create
            if self.path.startswith('/user/create'):
                user_data = User(username=request_data.get(
                    'username'), password=request_data.get('password'))
                response = await self.user_controller.create_user(
                    user_data.username, user_data.password)

            # group create
            elif self.path.startswith('/group'):
                # Authentication check
                if not authenticate_user(auth_header):
                    self.send_error(401, "Unauthorized")
                    return
                if self.path == '/group/create':
                    group_data = Group(name=request_data.get('name'))
                    response = await self.group_controller.create_group(
                        group_data.name)
                else:
                    response = {"error": "Endpoint not found"}

            # Authentication
            elif self.path.startswith('/authenticate'):
                if authenticate_check(request_data):
                    jwt_token = generate_jwt_token(request_data['username'])
                    response = {"jwt_token": jwt_token}
                else:
                    response = {"error": "Authentication failed"}

            # dataset create
            elif self.path == '/dataset/create':
                dataset_data = EntDataset(**request_data)
                response = self.dataset_controller.create_dataset(
                    dataset_data.name, dataset_data.description, dataset_data.created_by)

            # metadata create
            elif self.path.startswith('/metadata/create'):
                metadata_data = request_data
                response = await self.metadata_controller.create_metadata(
                    metadata_data['name'], metadata_data['value'])

            # filelist create
            elif self.path.startswith('/filelist/create'):
                token = self.headers.get('Authorization')
                if not token:
                    self.send_error(401, "Unauthorized: JWT token missing")
                    return
                try:
                    decoded_token = jwt.decode(
                        token, SECRET_KEY, algorithms=['HS256'])
                    creator_username = decoded_token['username']
                except jwt.ExpiredSignatureError:
                    self.send_error(401, "Unauthorized: JWT token expired")
                    return
                except jwt.InvalidTokenError:
                    self.send_error(401, "Unauthorized: Invalid JWT token")
                    return

                filelist_controller = FilelistController()
                filelist_data = EntFilelist(name=request_data.get(
                    'name'), description=request_data.get('description'))
                response = await filelist_controller.create_filelist(
                    filelist_data, creator_username)

            # annotation store
            elif self.path == '/store_annotation_result':
                annotation_controller = AnnotationController()
                response = await annotation_controller.store_annotation_result(request_data)

            # annotation retrieve
            elif self.path == '/retrieve_annotation_data':
                annotation_controller = AnnotationController()
                response = await annotation_controller.retrieve_annotation_data(request_data.get('recording_id'))

            # data processing
            elif self.path == '/clean_and_preprocess_data':
                data_processing_controller = DataProcessingController()
                response = await data_processing_controller.clean_and_preprocess_data(request_data.get('model_id'))
            elif self.path == '/quality_checks':
                data_processing_controller = DataProcessingController()
                response = await data_processing_controller.quality_checks(request_data.get('model_id'))

            else:
                response = {"error": "Endpoint not found"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError as e:
            print("Error decoding JSON data:", e)
            self.send_error(400, "Bad Request: Invalid JSON data")

        except Exception as e:
            print("Error processing request:", e)
            self.send_error(500, "Internal Server Error")

    async def do_GET(self):
        try:
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_error(400, "Bad Request: Empty request body")
                return

            auth_header = self.headers.get('Authorization')
            post_data = self.rfile.read(content_length)
            request_data = await json.loads(post_data.decode('utf-8'))

            # user read
            if self.path.startswith('/user/details'):
                user_id = int(self.path.split('/')[-1])
                # Logic to retrieve user details based on user ID
                user_details = self.user_controller.get_user_details(user_id)
                response = await {"user_details": user_details}

            # group read
            elif self.path.startswith('/group/details'):
                group_id = int(self.path.split('/')[-1])
                # Logic to retrieve group details based on group ID
                group_details = self.group_controller.get_group_details(
                    group_id)
                response = await {"group_details": group_details}

            # dataset read
            elif self.path.startswith('/dataset/read'):
                dataset_id = int(self.path.split('/')[-1])
                response = await self.dataset_controller.get_dataset(dataset_id)

            elif self.path.startswith('/filelist/read'):
                filelist_id = int(self.path.split('/')[-1])
                response = await self.filelist_controller.get_filelist(filelist_id)

            # annotation read
            elif self.path.startswith('/annotation/read'):
                annotation_id = int(self.path.split('/')[-1])
                response = await self.annotation_controller.get_annotation(annotation_id)

            # data processing
            elif self.path.startswith('/model/read'):
                model_id = int(self.path.split('/')[-1])
                response = await self.data_processing_controller.get_model(model_id)

            # metadata read
            elif self.path.startswith('/metadata/read'):
                metadata_id = int(self.path.split('/')[-1])
                response = await self.metadata_controller.get_metadata(metadata_id)

            else:
                response = {"error": "Endpoint not found"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print("Error processing request:", e)
            self.send_error(500, "Internal Server Error")

    async def do_PUT(self):
        try:
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_error(400, "Bad Request: Empty request body")
                return

            auth_header = self.headers.get('Authorization')
            data = self.rfile.read(content_length)
            request_data = json.loads(data.decode('utf-8'))
            path = self.path

            # user update
            if path.startswith('/user/update'):
                user_id = int(self.path.split('/')[-1])
                await self.user_controller.update_user(
                    user_id, request_data['username'], request_data['password'])
                response = {"message": "User updated succesfully"}

            # group update
            elif path.startswith('/group/update'):
                group_id = int(self.path.split('/')[-1])
                await self.group_controller.update_group(
                    group_id, request_data['name'])
                response = {"message": "Group updated successfully"}

            # dataset update
            elif self.path.startswith('/dataset/update'):
                dataset_id = int(self.path.split('/')[-1])
                dataset_data = EntDataset(**request_data)
                response = await self.dataset_controller.update_dataset(
                    dataset_id, dataset_data.name, dataset_data.description)

            # metadata update
            elif self.path.startswith('/metadata/update'):
                metadata_id = int(self.path.split('/')[-1])
                metadata_data = request_data
                response = await self.metadata_controller.update_metadata(
                    metadata_id, metadata_data['name'], metadata_data['value'])

            # data processing
            elif self.path.startswith('/model/update'):
                model_id = int(self.path.split('/')[-1])
                model_data = request_data
                response = await self.data_processing_controller.update_model(
                    model_id, model_data['name'], model_data['description'])

            # filelist update
            elif self.path.startswith('/filelist/update'):
                filelist_id = int(self.path.split('/')[-1])
                filelist_data = EntFilelist(**request_data)
                response = await self.filelist_controller.update_filelist(
                    filelist_id, filelist_data.name, filelist_data.description)

            # annotation update
            elif self.path.startswith('/annotation/update'):
                annotation_id = int(self.path.split('/')[-1])
                annotation_data = request_data
                response = await self.annotation_controller.update_annotation(
                    annotation_id, annotation_data['recording_id'], annotation_data['start_time'], annotation_data['end_time'], annotation_data['label_id'])

            else:
                response = {"error": "Endpoint not found"}

            if response:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

        except json.JSONDecodeError as e:
            print("Error decoding JSON data:", e)
            self.send_error(400, "Bad Request: Invalid JSON data")
        except Exception as e:
            print("Error processing request:", e)
            self.send_error(500, "Internal Server Error")

    async def do_DELETE(self):
        try:
            content_length = int(self.headers['Content-Length'])
            if content_length == 0:
                self.send_error(400, "Bad Request: Empty request body")
                return

            auth_header = self.headers.get('Authorization')
            data = self.rfile.read(content_length)
            request_data = json.loads(data.decode('utf-8'))

            # user delete
            if self.path.startswith('/user/delete'):
                user_id = int(self.path.split('/')[-1])
                await self.user_controller.delete_user(user_id)
                deleted = True
                if deleted:
                    response = {"message": "User deleted successfully"}
                else:
                    response = {"error": "User not found"}

            # group delete
            elif self.path.startswith('/group/delete'):
                group_id = int(self.path.split('/')[-1])
                await self.group_controller.delete_group(group_id)
                deleted = True
                if deleted:
                    response = {"message": "Group deleted successfully"}
                else:
                    response = {"error": "Group not found"}

            # dataset delete
            elif self.path.startswith('/dataset/delete'):
                dataset_id = int(self.path.split('/')[-1])
                response = await self.dataset_controller.delete_dataset(dataset_id)

            # metadata delete
            elif self.path.startswith('/metadata/delete'):
                metadata_id = int(self.path.split('/')[-1])
                response = await self.metadata_controller.delete_metadata(
                    metadata_id)

            # data processing
            elif self.path.startswith('/model/delete'):
                model_id = int(self.path.split('/')[-1])
                response = await self.data_processing_controller.delete_model(
                    model_id)

            # filelist delete
            elif self.path.startswith('/filelist/delete'):
                filelist_id = int(self.path.split('/')[-1])
                response = await self.filelist_controller.delete_filelist(filelist_id)

            elif self.path.startswith('/annotation/delete'):
                annotation_id = int(self.path.split('/')[-1])
                response = await self.annotation_controller.delete_annotation(
                    annotation_id)

            else:
                response = {"error": "Endpoint not found"}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            print("Error processing request:", e)
            self.send_error(500, "Internal Server Error")


def authenticate_user(auth_header):
    if not auth_header or not auth_header.startswith("Bearer "):
        return False
    jwt_token = auth_header.split(" ")[1]

    try:
        decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        print("JWT token has expired")
    except jwt.InvalidTokenError:
        print("Invalid JWT token")
    return False


def generate_jwt_token(username):
    payload = {"username": username}
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jwt_token


def authenticate_check(request_data):
    username = request_data.get('username')
    password = request_data.get('password')

    try:
        sql_config = get_sql_config()
        conn = mysql.connector.connect(**sql_config)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT username, password FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if user_data:
            if user_data[1] == password:
                return True
    except mysql.connector.Error as err:
        print("Error accessing database:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    # Authentication failed
    return False


async def run_server(port=8000):
    try:
        # asyncio.create_task(create_database())
        server_address = ('', port)
        server = await asyncio.start_server(RequestHandler, *server_address)
        print(f"Server running on port {port}")

        async with server:
            await server.serve_forever()

    except Exception as e:
        print("Error starting server:", e)



if __name__ == '__main__':
    run_server()
