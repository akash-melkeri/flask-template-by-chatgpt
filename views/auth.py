from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/api/auth')
db = None

@bp.route('/login')
def login():
    print('login')
    pass