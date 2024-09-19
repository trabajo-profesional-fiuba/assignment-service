import pytest

from src.config.config import api_config
from src.core.azure_container_client import AzureContainerClient


class TestAzureContainerClient:

    @pytest.mark.unit
    def test_azure_container_client_exists(self):
        # Arrange
        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )

        # Act & Assert
        assert az_client.exists() is True

    @pytest.mark.integration
    def test_upload_test_file_to_azure(self):

        # Arrange
        filename = "test_data.txt"
        file_path = "tests/unit/core/test_data.txt"
        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )

        with open(file_path, "rb") as file:
            content = file.read()

        blob = az_client.upload(content, filename)

        assert blob.blob_name == filename

    @pytest.mark.integration
    def test_download_test_file_to_azure(self):

        # Arrange
        filename = "test_data.txt"
        outputfilename = "C:/dev/uba/assignment-service/tests/unit/core/download.txt"

        expected_content = (
            "This is a txt file just for uploading and downloading for azure storage"
        )
        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(
            container=container_name, access_key=access_key
        )

        az_client.download(filename, outputfilename)

        # Open the file and read its content
        with open(outputfilename, "r") as file:
            file_content = file.read().strip()  # Remove any leading/trailing whitespace

        # Assert that the content matches the expected content
        assert (
            file_content == expected_content
        ), f"Content does not match. Expected: '{expected_content}', Found: '{file_content}'"
