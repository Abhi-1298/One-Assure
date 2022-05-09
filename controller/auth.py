import uuid
import json
from flask import abort, g
from functools import wraps

from models.models import User, Session, db, app

# random acess_token generated
def get_access_token():
    uid = uuid.uuid1()
    return uid.__str__()


# used for Decorator (Authentication)
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if g.is_authenticated is False:
            abort(401)
        else:
            return f(*args, **kws)
    return decorated_function


def login(request):
    body = request.get_json()
    user = User.query.filter(User.username == body['username']).first()

    if user:
        # login
        print(user.id)
        new_access_token = get_access_token()
        temp_session = Session(new_access_token, int(user.id))
        db.session.add(temp_session)
        db.session.commit()

        resp_data = {
            "message": "logedin successfully",
            "access_token": new_access_token,
            "username": user.username
        }

        response = app.response_class(
            status=200,
            response=json.dumps(resp_data),
            mimetype='application/json'
        )
        return response

    else:
        response = app.response_class(
            status=403,
            response=json.dumps(
                {"message": "username or password isn't valid"}),
            mimetype='application/json'
        )
        return response

# Logout


def logout(request):
    """
    acess_token should deleted..

    """
    access_token = request.headers.get("Authorization")  # acess_token got from headers from logout api
    Session.query.filter(Session.access_token == access_token).delete()
    db.session.commit()
    resp_data = {
        "message": "Logout successfully",
    }
    response = app.response_class(
        status=200,
        response=json.dumps(resp_data),
        mimetype='application/json'
    )
    return response
