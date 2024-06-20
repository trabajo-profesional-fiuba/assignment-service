from flask import Flask
from flasgger import Swagger
from api.routes import routes

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
