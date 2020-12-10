"""
Run this file to start rapi_site and api server
"""
from rapi_site import create_app
from rapi import create_app as create_api_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

rapi_service = create_api_app()
rapi_site = create_app()

application = DispatcherMiddleware(
    rapi_service, {
        '/rapi-site': rapi_site
    }
)

if __name__ == '__main__':
    run_simple(
        hostname='localhost',
        port=5000,
        application=application,
        use_reloader=True,
        use_debugger=True,
        use_evalex=True
    )
