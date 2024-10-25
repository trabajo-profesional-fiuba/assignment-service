import re
from typing import IO, Any, Iterable
from azure.storage.blob import BlobClient, ContainerClient, BlobPrefix


class AzureContainerClient:

    def __init__(self, access_key: str, container: str) -> None:
        self._access_key = access_key
        self._container = container

    def _get_container_client(self) -> ContainerClient:
        conn_str = self._access_key
        container_name = self._container
        container_client = ContainerClient.from_connection_string(
            conn_str=conn_str, container_name=container_name
        )

        return container_client

    def _matches_pattern(self, blobname: str, pattern: str | None = None) -> bool:

        return pattern is None or bool(re.match(pattern, blobname))

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

    def download(self, blob_name: str) -> bytes:
        container_client = self._get_container_client()
        stream_downloader = container_client.download_blob(blob=blob_name)
        content = stream_downloader.readall()
        return content

    def _walk_blob_hierarchy(
        self,
        container_client: ContainerClient,
        blobs: list,
        prefix: str | None = None,
        pattern: str | None = None,
        **kwargs: Any
    ):
        for blob in container_client.walk_blobs(name_starts_with=prefix, **kwargs):
            if isinstance(blob, BlobPrefix):
                self._walk_blob_hierarchy(
                    container_client, prefix=blob.name, pattern=pattern, blobs=blobs
                )
            else:
                if self._matches_pattern(blob.name, pattern):
                    blobs.append(blob)

        return blobs

    def list_blobs(
        self, prefix: str | None = None, pattern: str | None = None, **kwargs: Any
    ):
        container_client = self._get_container_client()
        blobs = self._walk_blob_hierarchy(
            container_client, blobs=list(), prefix=prefix, pattern=pattern
        )

        return blobs
