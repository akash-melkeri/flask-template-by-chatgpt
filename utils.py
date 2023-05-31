import flask
import json, jwt, logging, sys
from werkzeug.exceptions import HTTPException
import time
from functools import wraps
from bson import ObjectId
from datetime import datetime
import config

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_stderr = logging.getLogger('error_logger')
logger_stdout = logging.getLogger(__name__)
logger_stdout.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)
logger_stdout.addHandler(stdout_handler)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%SZ')
        return json.JSONEncoder.default(self, o)

def unauthorized_abort():
    return flask.abort(401)

def dictify_document(doc):
    return doc.to_mongo().to_dict()
  
def requires_auth(role=None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'USER_ID' not in flask.session:
                return unauthorized_abort()
            else:
                if role is not None:
                    if isinstance(role, list):
                        flag = 0
                        for each in role:
                            if not flask.session['ROLES'] or each not in flask.session['ROLES']:
                                flag = 0
                            else:
                                flag = 1
                                break
                        if flag == 0:
                            return unauthorized_abort()
                    elif role not in flask.session['ROLES']:
                        return unauthorized_abort()
                return f(*args, **kwargs)
        return decorated
    return wrapper

def verify_token():
    auth_doesnt_matter_routes = [
        "/api/auth/login"
    ]
    for_both_routes = [
        "/api/tool/submit"
    ]
    if(flask.request.path in for_both_routes):
        setattr(flask.request,"user_data",False)
        auth_header = flask.request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split(" ")[-1]
            try:
                decoded_token = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
                if(datetime.fromtimestamp(decoded_token.get('expires')) < datetime.now()):
                    flask.abort(401,"Expired")
                setattr(flask.request,"user_data",decoded_token)
            except:
                flask.abort(401,"SOMETHING BADLY WENT WRONG")
        
    elif flask.request.path not in auth_doesnt_matter_routes:
        auth_header = flask.request.headers.get("Authorization")
        if not auth_header:
            flask.abort(401,"Access denied")
        token = auth_header.split(" ")[-1]
        try:
            decoded_token = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
            if(datetime.fromtimestamp(decoded_token.get('expires')) < datetime.now()):
                flask.abort(401,"Expired")
            setattr(flask.request,"user_data",decoded_token)
        except:
            flask.abort(401,"Invalid request")

def signJWT(email: str, username: str, image:str):
    payload = {
        "email": email,
        "username": username,
        "image": image,
        "expires": time.time() + 86400
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)

    return token


def unhandled_exception(error):
    logger_stderr.error("%s - ERROR - Exception occured" % str(datetime.utcnow()), exc_info=True)
    res = flask.jsonify(ok=True)
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    res.status_code = code
    return res