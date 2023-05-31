from flask import Blueprint
from models import db

bp = Blueprint('views', __name__)
from views import auth, user
auth.db = user.db = db

bp.register_blueprint(auth.bp, url_prefix='/api/auth')
bp.register_blueprint(user.bp, url_prefix='/api/user')