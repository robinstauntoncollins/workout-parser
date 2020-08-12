from flask import Flask, make_response
from flask_migrate import Migrate

from config import config

from .models import db

from workout.api.v1 import api_v1_bp, API_VERSION_V1
from workout.intentapi import intent_api_bp


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = 'default'
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print(f"App Config: {app.config}")

    db.init_app(app)
    _ = Migrate(app, db)

    app.register_blueprint(
        api_v1_bp,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )

    app.register_blueprint(
        intent_api_bp,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )

    @app.route('/')
    def index():
        from workout.api.v1 import get_catelog as v1_collections_catelog
        from workout.intentapi import get_catelog as v1_actions_catelog
        return {
            'version': {
                'v1': {
                    'collections': v1_collections_catelog(),
                    'actions': v1_actions_catelog()
                }
            }
        }

    @app.errorhandler(400)
    def bad_request(error):
        return make_response({'error': 'Bad request'}, 400)

    @app.errorhandler(404)
    def not_found(error):
        return make_response({'error': 'Not found'}, 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return make_response({'error': 'Method not allowed'}, 405)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response({'error': 'Internal Server Error'}, 500)

    return app
