from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_assets import Environment
from flask_login import current_user
from flask_restless import APIManager, ProcessingException

from garden.models import User

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


# Create the Flask-Restless API manager.
api_manager = APIManager()


def auth_func(**kw):
    if not current_user.is_authenticated():
        raise ProcessingException(description='Not Authorized', code=401)


