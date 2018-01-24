#! ../env/bin/python

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader
from garden import assets
from garden.models import db, test_user
from garden.controllers.main import main

from garden.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager,
    api_manager,
    auth_func,
    admin
)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. garden.settings.ProdConfig
    """

    app = Flask(__name__)

    app.config.from_object(object_name)

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy if necessary
    # print("No database currently. Building user.")
    # build_sample_db()

    db.init_app(app)

    # initialize flask_login
    login_manager.init_app(app)

    # initialize flask_restless
    api_manager.init_app(app, flask_sqlalchemy_db=db)

    # initialize the admin UI
    admin.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)


    return app


def build_sample_db():
    db.create_all()
    db.session.add(test_user)


