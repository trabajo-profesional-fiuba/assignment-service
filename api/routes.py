from flask import Blueprint

routes = Blueprint("routes", __name__)


@routes.route("/")
def ping():
    """
    A simple endpoint that returns "Ping" to check system's availability
    ---
    responses:
      200:
        description: A successful response
        content:
          text/plain:
            schema:
              type: string
    """
    return "Ping"
