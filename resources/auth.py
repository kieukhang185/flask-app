from flask_restx import Namespace, Resource, fields
from extensions import bcrypt, mongo
from flask_jwt_extended import create_access_token
api = Namespace('auth', description='Authentication')
user_model = api.model('UserAuth', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})
@api.route('/login')
class Login(Resource):
    @api.expect(user_model)
    def post(self):
        data = api.payload
        user = mongo.db.users.find_one({'username': data['username']})
        if not user or not bcrypt.check_password_hash(user['password'], data['password']):
            api.abort(401, 'Invalid credentials')
        token = create_access_token(identity=str(user['_id']))
        return {'access_token': token}