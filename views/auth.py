from flask_restx import Resource, Namespace
from implemented import auth_service
from flask import request, abort

auth_ns = Namespace('auth')

@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        rej = request.json
        username = rej.get('username')
        password = rej.get('password')
        if None in [username, password]:
            abort(401)

        tokens = auth_service.gen_token(username, password)
        return tokens, 201

    def put(self):
        rej = request.json
        refresh_token = rej.get('refresh_token')
        tokens = auth_service.appruve_revresh(refresh_token)
        return tokens, 201
