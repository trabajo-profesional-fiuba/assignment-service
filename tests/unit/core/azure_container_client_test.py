import pytest

from src.config.config import api_config
from src.core.azure_container_client import AzureContainerClient

class TestAzureContainerClient:

    @pytest.mark.unit
    def test_azure_container_client_exists(self):
        # Arrange
        container_name = api_config.container
        access_key = api_config.storage_access_key
        az_client = AzureContainerClient(container=container_name, access_key=access_key)

        # Act & Assert 
        assert az_client.exists() is True