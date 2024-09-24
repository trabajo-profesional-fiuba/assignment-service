from typing import IO, Iterable
from azure.storage.blob import BlobClient, ContainerClient


class AzureContainerClient:

    def __init__(self, access_key: str, container: str) -> None:
        self._access_key = access_key
        self._container = container

    def _get_container_client(self):
        conn_str = self._access_key
        container_name = self._container
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_str, container_name=container_name
        )

        return container_client

    def exists(self) -> bool:
        container_client = self._get_container_client()
        return container_client.exists()

    def upload(
        self, data: bytes | str | Iterable | IO, filename: str, overwrite: bool
    ) -> BlobClient:
        container_client = self._get_container_client()
        blob = container_client.upload_blob(
            data=data, name=filename, overwrite=overwrite
        )

        return blob

    def download(self, blob_name: str)-> bytes:
        container_client = self._get_container_client()
        stream_downloader = container_client.download_blob(blob=blob_name)
        content = stream_downloader.readall()

        return content
