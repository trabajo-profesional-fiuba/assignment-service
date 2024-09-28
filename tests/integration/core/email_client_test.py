import os
import pytest
from src.config.config import api_config
from src.core.email_client import SendGridEmailClient


class TestEmailClient:

    # skip test so we dont send spam emails
    @pytest.mark.skip
    def test_send_email_to_user(self):
        api_key = api_config.email_key
        email_client = SendGridEmailClient(api_key)
        response = email_client.send_email(
            "avillores@fi.uba.ar ",
            "Mensaje importante para Agus",
            "Hola como andas?",
        )
        assert response == 202

    @pytest.mark.skip
    def test_send_api_withou_key_raise_exception(self):
        email_client = SendGridEmailClient()
        with pytest.raises(Exception):
            response = email_client.send_email("test@fiuba.com", "Test FIUBA", "body")

    @pytest.mark.skip
    def test_send_email_to_multiple_users(self):
        api_key = api_config.email_key
        email_client = SendGridEmailClient(api_key)
        users = [
            "vlopez@fi.uba.ar",
            "ipfaab@fi.uba.ar",
            "cdituro@fi.uba.ar",
            "joagomez@fi.uba.ar",
        ]
        response = email_client.send_emails(
            users, "Test FIUBA", "Esto es una prueba no responder"
        )
        assert response == 202
