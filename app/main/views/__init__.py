import os
from flask import send_from_directory, current_app as app
from .. import main

from .index import *
from .user import *
from .post import *
from .follow import *


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/vnd.microsoft.icon')