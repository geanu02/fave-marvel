from flask import Flask
from config import Config
from marvel import Marvel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
login = LoginManager(app)

login.login_view = 'auth.signin'
login.login_message = "Login required"
login.login_message_category = "warning"

marvel_obj = Marvel(PUBLIC_KEY=Config.API_PUB_KEY, PRIVATE_KEY=Config.API_PRIV_KEY)

from app.blueprints.main import bp as main_bp
app.register_blueprint(main_bp)
from app.blueprints.marvel import bp as marvel_bp
app.register_blueprint(marvel_bp)
from app.blueprints.auth import bp as auth_bp
app.register_blueprint(auth_bp)
# from app.blueprints.api import bp as api_bp
# app.register_blueprint(api_bp)

from app import models