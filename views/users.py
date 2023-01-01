from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')

@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        rs = user_service.get_all()
        res = UserSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        rej = request.json
        rs = user_service.create(rej)
        return '', 201, {'location': f'/users/{rs.id}'}



@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        rs = user_service.get_one(uid)
        res = UserSchema().dump(rs)
        return res, 200

    def put(self, uid):
        rej = request.json
        if 'id' not in rej:
            rej['id'] = uid
        user_service.update(rej)
        return '', 204

    def delete(self, uid):
        user_service.delete(uid)
        return '', 204
