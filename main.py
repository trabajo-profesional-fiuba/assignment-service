import uvicorn
from src.config.config import api_config
from src.api.app import app

if __name__ == "__main__":
    host = api_config.host
    port = api_config.port


    print(f"Host: {host}")
    print(f"Port: {port}")

    try:
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("Server stopped manually.")