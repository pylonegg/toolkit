from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobServiceClient
import logging

def get_clients(subscription_id: str):
    cred = DefaultAzureCredential()
    return {
        "rg": ResourceManagementClient(cred, subscription_id),
        "auth": AuthorizationManagementClient(cred, subscription_id),
        "storage": StorageManagementClient(cred, subscription_id),
    }



def blob_service_client(conn_str, label):
    try:
        client = BlobServiceClient.from_connection_string(conn_str)
        logging.info(f"Connected to {label} storage successfully.")
        return client
    except Exception as e:
        logging.error(f"Failed to connect to {label} storage: {e}")
        exit(1)
