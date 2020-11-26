from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rapi_site.database import db_session

bp = Blueprint('r_map', __name__)


@bp.route('/')
def index():
    return render_template('r_map/index.html')
