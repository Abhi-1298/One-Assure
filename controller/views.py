from flask import g
from sqlalchemy.exc import IntegrityError
from models.models import db, User, File, Column
import pandas as pd
import json

from models.models import User, db, app
from controller import auth


def create_user(request):
    body = request.get_json()
    user = User(body['username'], body['email'], body['password'])
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return app.response_class(
            status=409,
            response=json.dumps({"message": "username already exist"}),
            mimetype='application/json'
        )

    response = {
        "message": "user created successfully"
    }

    return app.response_class(
        status=200,
        response=json.dumps(response),
        mimetype='application/json'
    )


def file_upload(request):
    file = request.files['file']
    if file:
        if '.csv' in file.filename:
            # reading csv file
            df = pd.read_csv(file)

            data = df.to_dict()

            file_instance = File(filename=file.filename)  # <- file id

            for colname in data:
                for row_idx in data[colname]:
                    column = Column(col_name=colname, row_pos=row_idx,
                                    col_row_data=data[colname][row_idx])
                    file_instance.columns.append(column)

            db.session.add(file_instance)
            db.session.commit()

            response = {
                "message": "file uploaded successfully"
            }
            return app.response_class(
                status=200,
                response=json.dumps(response),
                mimetype='application/json'
            )
    response = {
        "message": "provide a valid file"
    }
    return app.response_class(
        status=400,
        response=json.dumps(response),
        mimetype='application/json'
    )


def file_lookup(request, column_name, column_value):
    """ Lookup through all csv files column """

    qdata = Column.query.filter(Column.col_name == column_name).filter(
        Column.col_row_data == column_value)
    master_data = {}
    for file in qdata.all():
        # print(r, r.file_id, r.row_pos)
        rows = Column.query.filter(Column.file_id == file.file_id).filter(
            Column.row_pos == file.row_pos).all()
        temp_dict = {row.col_name: row.col_row_data for row in rows}

        # conditions
        if file.file_id not in master_data:
            master_data[file.file_id] = {
                "file_name": File.query.get(file.file_id).filename,
                "file_data": [temp_dict]
            }
        else:
            master_data[file.file_id]["file_data"].append(temp_dict)

    return app.response_class(
        status=200,
        response=json.dumps(master_data),
        mimetype='application/json'
    )


def file_lookup_delete(request, search_flie_name):

    try:
        all = File.query.filter(File.filename.like(
            f"%{search_flie_name}%")).all()
        for file in all:
            db.session.query(Column).filter(Column.file_id == file.id).delete()
            db.session.query(File).filter(File.id == file.id).delete()
        db.session.commit()
    except Exception as E:
        print("Exception ==  ", E)
        db.session.rollback()

    response = {
        "message": "Successfully deleted"
    }

    return app.response_class(
        status=200,
        response=json.dumps(response),
        mimetype='application/json'
    )
