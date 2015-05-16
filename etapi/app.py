# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from etapi.settings import ProdConfig
from etapi.assets import assets
from etapi.extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    debug_toolbar,
)
from etapi.utils import (
    pretty_date,
    pretty_seconds_to_hh,
    pretty_seconds_to_hhmm,
    pretty_seconds_to_hhmmss
)

from .public import public
from .weather import weather
from .charts import charts


DEFAULT_BLUEPRINTS = (
    public,
    weather,
    charts,
)

def create_app(config_object=ProdConfig, blueprints=None):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app, blueprints)
    register_errorhandlers(app)
    configure_template_filters(app)

    return app


def register_extensions(app):
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app, blueprints):
    """
    Register blueprints in views.
    """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return None


def configure_template_filters(app):

    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter('pretty_seconds_hh')
    def pretty_seconds_to_hh_filter(value):
        return pretty_seconds_to_hh(value)

    @app.template_filter('pretty_seconds_hhmm')
    def pretty_seconds_to_hhmm_filter(value):
        return pretty_seconds_to_hhmm(value)

    @app.template_filter('pretty_seconds_hhmmss')
    def pretty_seconds_to_hhmm_filter(value):
        return pretty_seconds_to_hhmmss(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
