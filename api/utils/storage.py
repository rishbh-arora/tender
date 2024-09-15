import requests
from google.cloud import storage
import io

client = storage.Client()

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return io.BytesIO(response.content)

def upload_to_gcs(file_stream, bucket_name, destination_blob_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_stream, content_type='application/zip')
    blob.make_public()
    print(f'File {destination_blob_name} uploaded to {bucket_name}.')
    return blob.public_url