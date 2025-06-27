from flask_restx import Namespace, Resource, fields
from extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
api = Namespace('user', description='User operations')
user_model = api.model('User', {
    'username': fields.String,
    'email': fields.String,
    'role': fields.String,
})
@api.route('/')
class Users(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return list(mongo.db.users.find({}, {'password':0}))

@api.route('/profile')
class Profile(Resource):
    @jwt_required()
    @api.marshal_with(user_model)
    def get(self):
        uid = get_jwt_identity()
        user = mongo.db.users.find_one({'_id': ObjectId(uid)})
        return user