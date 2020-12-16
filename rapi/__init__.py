import connexion

from rapi.autogen.openapi_server import encoder


def create_app():
    app = connexion.App(__name__)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('open_api/rapi-service.yaml')
    return app


if __name__ == '__main__':
    rapi = create_app()
    rapi.run(port=8080, debug=True)

