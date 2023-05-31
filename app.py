from flask import Flask
from views import bp as views_bp
from models import db
from utils import JSONEncoder, verify_token, unhandled_exception

app = Flask(__name__)
views_bp.db = db

app.config.from_pyfile('config.py')
app.json_encoder = JSONEncoder
app.before_request(verify_token)
app.errorhandler(unhandled_exception)
app.register_blueprint(views_bp)

if __name__ == '__main__':
    app.run(port=6001)