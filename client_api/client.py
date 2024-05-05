import requests
from .exceptions import APIError

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, username, password):
        endpoint = f"{self.base_url}/create_user"
        data = {"username": username, "password": password}
        response = requests.post(endpoint, json=data)
        return self._handle_response(response)

    def get_user(self, user_id):
        endpoint = f"{self.base_url}/get_user/{user_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def update_user(self, user_id, new_username, new_password):
        endpoint = f"{self.base_url}/update_user/{user_id}"
        data = {"new_username": new_username, "new_password": new_password}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)

    def delete_user(self, user_id):
        endpoint = f"{self.base_url}/delete_user/{user_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)
    
    def create_group(self, name):
        endpoint = f"{self.base_url}/create_group"
        data = {"name": name}
        response = requests.post(endpoint, json=data)
        return self._handle_response(response)

    def get_group(self, group_id):
        endpoint = f"{self.base_url}/get_group/{group_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)
    
    def update_group(self, group_id, new_name):
        endpoint = f"{self.base_url}/update_group/{group_id}"
        data = {"new_name": new_name}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)

    def delete_group(self, group_id):
        endpoint = f"{self.base_url}/delete_group/{group_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)

    def create_dataset(self, name, description, created_by):
        endpoint = f"{self.base_url}/create_dataset"
        data = {"name": name, "description": description, "created_by": created_by}
        response = requests.post(endpoint, json=data)
        return self._handle_response(response)

    def get_dataset(self, dataset_id):
        endpoint = f"{self.base_url}/get_dataset/{dataset_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def update_dataset(self, dataset_id, new_name, new_description):
        endpoint = f"{self.base_url}/update_dataset/{dataset_id}"
        data = {"new_name": new_name, "new_description": new_description}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)

    def delete_dataset(self, dataset_id):
        endpoint = f"{self.base_url}/delete_dataset/{dataset_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)

    def create_filelist(self, name, description):
        endpoint = f"{self.base_url}/create_filelist"
        data = {"name": name, "description": description}
        response = requests.post(endpoint, json=data)
        return self._handle_response(response)

    def get_filelist(self, filelist_id):
        endpoint = f"{self.base_url}/get_filelist/{filelist_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def update_filelist(self, filelist_id, new_name, new_description):
        endpoint = f"{self.base_url}/update_filelist/{filelist_id}"
        data = {"new_name": new_name, "new_description": new_description}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)

    def delete_filelist(self, filelist_id):
        endpoint = f"{self.base_url}/delete_filelist/{filelist_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)

    def store_annotation_result(self, annotation_data):
        endpoint = f"{self.base_url}/store_annotation_result"
        response = requests.post(endpoint, json=annotation_data)
        return self._handle_response(response)

    def retrieve_annotation_data(self, recording_id):
        endpoint = f"{self.base_url}/retrieve_annotation_data/{recording_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def get_jwt_token(self, username):
        endpoint = f"{self.base_url}/get_jwt_token"
        data = {"username": username}
        response = requests.post(endpoint, json=data)
        return self._handle_response(response)

    def get_metadata(self, metadata_id):
        endpoint = f"{self.base_url}/get_metadata/{metadata_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def update_metadata(self, metadata_id, new_name, new_description):
        endpoint = f"{self.base_url}/update_metadata/{metadata_id}"
        data = {"new_name": new_name, "new_description": new_description}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)

    def delete_metadata(self, metadata_id):
        endpoint = f"{self.base_url}/delete_metadata/{metadata_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)

    def get_recording(self, recording_id):
        endpoint = f"{self.base_url}/get_recording/{recording_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)

    def update_recording(self, recording_id, new_name, new_description):
        endpoint = f"{self.base_url}/update_recording/{recording_id}"
        data = {"new_name": new_name, "new_description": new_description}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)
    
    def delete_recording(self, recording_id):
        endpoint = f"{self.base_url}/delete_recording/{recording_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)
    
    def get_model(self, model_id):
        endpoint = f"{self.base_url}/get_model/{model_id}"
        response = requests.get(endpoint)
        return self._handle_response(response)
    
    def update_model(self, model_id, new_name, new_description):
        endpoint = f"{self.base_url}/update_model/{model_id}"
        data = {"new_name": new_name, "new_description": new_description}
        response = requests.put(endpoint, json=data)
        return self._handle_response(response)
    
    def delete_model(self, model_id):
        endpoint = f"{self.base_url}/delete_model/{model_id}"
        response = requests.delete(endpoint)
        return self._handle_response(response)

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Error: {response.status_code} - {response.reason}"
            raise APIError(error_message)

# Initialize the client with the server's base URL
client = APIClient("http://localhost:8000")
