from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class AzureContainerClient:

    def __init__(self, access_key: str, container: str) -> None:
        self._access_key = access_key
        self._container = container

    def exists(self):
        conn_str = self._access_key
        container_name = self._container
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_str, container_name=container_name
        )

        return container_client.exists()
