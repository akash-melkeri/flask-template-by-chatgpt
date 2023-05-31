from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/api/user')
db = None

@bp.route('/users',methods=["GET"])
def get_users():
    print("users")
    pass
