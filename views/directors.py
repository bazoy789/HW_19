from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from decorators import auth_required, admin_required
director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        rej = request.json
        rs = director_service.create(rej)
        return '', 201, {'location': f'/director/{rs.id}'}



@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, rid):
        rej = request.json
        if 'id' not in rej:
            rej['id'] = rid
        rs = director_service.update(rej)
        return '', 204

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return '', 204
