import pytest
from api.app import app


class TestRoutes:
    @pytest.fixture
    def client(self):
        app.testing = True
        with app.test_client() as client:
            yield client

    def test_ping(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.data.decode("utf-8") == "Ping"
