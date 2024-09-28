import os
import pytest
from src.config.config import api_config
from src.core.email_client import SendGridEmailClient

class TestEmailClient:

    @pytest.mark.integration
    def test_send_email_to_user(self):
        api_key = api_config.email_key
        email_client = SendGridEmailClient(api_key)
        response = email_client.send_email('alejovillores@gmail.com', 'Test FIUBA', 'Hola como andas?')
        assert response == 202
    
    @pytest.mark.integration
    def test_send_api_withou_key_raise_exception(self):
        email_client = SendGridEmailClient()
        with pytest.raises(Exception):
            response = email_client.send_email('test@fiuba.com', 'Test FIUBA', 'body')