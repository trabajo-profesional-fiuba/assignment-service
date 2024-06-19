from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/")
def hello_world():
    """
    A simple endpoint that returns "Hello, World!"
    ---
    responses:
      200:
        description: A successful response
        content:
          text/plain:
            schema:
              type: string
    """
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True, port=8080)
