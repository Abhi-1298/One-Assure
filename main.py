from flask import request, g

from controller import auth, views
from models.models import Session, app, User


@app.before_request
def middleware():
    "This middleware fucn sets user & authentication values"
    MAX_SESSION_TIME = 30  # minute
    g.is_authenticated = False  # until we verify the access_token

    access_token = request.headers.get("Authorization")
    if access_token != "":
        # when we have the access token
        # - check token in session_table and verify

        session = Session.query.filter(
            Session.access_token == access_token).first()

        if session:
            g.user = session.user
            g.is_authenticated = True


@app.route('/user', methods=['POST'])
def user():
    if request.method == "POST":
        return views.create_user(request)


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        return auth.login(request)


@app.route('/logout', methods=['GET'])
@auth.authenticate
def logout():
    if request.method == "GET":
        return auth.logout(request)


@app.route('/upload/file', methods=['POST'])
@auth.authenticate
def upload_file():
    if request.method == "POST":
        return views.file_upload(request)


@app.route('/file/<column_name>/<column_value>', methods=['GET'])
@auth.authenticate
def lookup_file(column_name, column_value):
    if request.method == "POST":
        return views.file_lookup(request, column_name, column_value)


@app.route('/file/<file_name>', methods=['DELETE'])
@auth.authenticate
def delete_lookup_file(file_name):
    return views.file_lookup_delete(request, file_name)


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
