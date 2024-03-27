from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from app.model import Dictionary

class LookupResource(Resource):
    def post(self):
        req = request.get_json()
        try:
            eng_def = Dictionary.query.filter_by(puflantu=req["word"]).scalar()
            if not eng_def:
                return { 'message': 'Unknown Puflantu word' },  404
            else: 
                return {'definition': eng_def.english}, 200
        except IntegrityError:
            return { 'message': 'Unexpected Error'}, 500