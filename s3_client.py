import boto3

class S3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        self.s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.bucket_name = bucket_name

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = file_name
        
        try:
            response = self.s3.upload_file(file_name, self.bucket_name, object_name)
            print(f"File uploaded successfully: {response}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def list_files(self):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name)
            if 'Contents' in response:
                files = [obj['Key'] for obj in response['Contents']]
                return files
            else:
                print("No files found in the bucket.")
        except Exception as e:
            print(f"Error listing files: {e}")

    def download_file(self, object_name, file_name):
        try:
            self.s3.download_file(self.bucket_name, object_name, file_name)
            print(f"File downloaded successfully: {file_name}")
        except Exception as e:
            print(f"Error downloading file: {e}")

# Example usage:
if __name__ == "__main__":
    client = S3Client(access_key='YOUR_ACCESS_KEY', secret_key='YOUR_SECRET_KEY', bucket_name='YOUR_BUCKET_NAME')
    
    client.upload_file('local_file.txt', 'remote_file.txt')
    
    files = client.list_files()
    print("Files in bucket:", files)
    
    client.download_file('remote_file.txt', 'downloaded_file.txt')
