"""
Run this file to start rapi_site and api server
"""
from rapi_site import create_app

rapi_site = create_app()
rapi_site.run(debug=True)
