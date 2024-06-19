from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/")
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
