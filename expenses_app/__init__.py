from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e5094686ac92054b2a9bb4371ba3283'
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from expenses_app.models import User

# Flask-Login konfiguracija
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from expenses_app import routes
