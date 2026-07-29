from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from flask_bcrypt import Bcrypt
from routes import auth

bcrypt = Bcrypt()

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    @app.route("/")
    def home():
        return "Secure Authentication System Running!"

    return app

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)