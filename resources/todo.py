from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('todo', description='ToDo operations')

todo_model = api.model('Todo', {
    'id' : fields.String(required=True, description='The primakey'),
    'key': fields.String(readonly=True, description='Generated key'),
    'title': fields.String(required=True),
    'description': fields.String,
    'status': fields.String(enum=['new','in-progress','reject','done','under-review'], default='new'),
    'label': fields.String,
    'reporter': fields.String(required=True),
    'assignee': fields.String,
    'type': fields.String(required=True, enum=['task','sub-task','epic','bug']),
    'epic': fields.String(description='Optional epic id'),
    'parent_task': fields.String(description='Required parent task id for sub-tasks'),
    'comments': fields.List(fields.String),
})

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, default=1)
parser.add_argument('per_page', type=int, default=20)

@api.route('/')
class TodoList(Resource):
    @api.expect(todo_model)
    @jwt_required()
    @api.marshal_with(todo_model, code=201)
    def post(self):
        data = api.payload
        # enforce parent_task for sub-tasks
        if data['type'] == 'sub-task':
            if not data.get('parent_task'):
                api.abort(400, 'parent_task is required for sub-task')
        # optional epic for tasks/bugs
        # generate key
        seq = mongo.db.todos.count_documents({'type': data['type']}) + 1
        prefix = {
            'task': 'TASK-', 'epic': 'EPIC-', 'sub-task': 'SUB-', 'bug': 'BUG-'
        }[data['type']]
        data['key'] = f"{prefix}{seq:02d}"
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        data['reporter'] = get_jwt_identity()
        result = mongo.db.todos.insert_one(data)
        new_id = result.inserted_id
        # prepare return document
        data['id'] = str(new_id)
        data.pop('_id', None)
        return data, 201

    @api.expect(parser)
    @api.marshal_with(todo_model, as_list=True)
    def get(self):
        args = parser.parse_args()
        page      = args.get('page', 1)
        per_page  = args.get('per_page', 10)

        cursor = (
            mongo.db.todos
                 .find()
                 .skip((page - 1) * per_page)
                 .limit(per_page)
        )
        todos = []
        for doc in cursor:
            # 1) inject a proper 'id' string
            doc['id'] = str(doc['_id'])
            # 2) remove the raw ObjectId field
            doc.pop('_id', None)
            todos.append(doc)

        return todos, 200

@api.route('/<string:id>')
class TodoResource(Resource):
    @api.marshal_with(todo_model)
    def get(self, id):
        t = mongo.db.todos.find_one({'_id': ObjectId(id)})
        if not t: api.abort(404, 'ToDo not found')
        t['id'] = str(t['_id'])
        t.pop('_id', None)
        return t

    @api.expect(todo_model)
    @api.marshal_with(todo_model)
    def put(self, id):
        data = api.payload
        # enforce parent_task for sub-tasks
        if data['type'] == 'sub-task':
            if not data.get('parent_task'):
                api.abort(400, 'parent_task is required for sub-task')
        data['updated_at'] = datetime.utcnow()
        mongo.db.todos.update_one({'_id': ObjectId(id)}, {'$set': data})
        updated = mongo.db.todos.find_one({'_id': ObjectId(id)})
        updated['id'] = str(updated['_id'])
        return updated

    def delete(self, id):
        mongo.db.todos.delete_one({'_id': ObjectId(id)})
        return '', 204

@api.route('/epics')
class EpicList(Resource):
    @api.marshal_with(todo_model, as_list=True)
    def get(self):
        epics = list(mongo.db.todos.find({'type': 'epic'}))
        for e in epics:
            e['id'] = str(e['_id'])
        return epics

@api.route('/<string:todo_id>/assign')
class TodoAssign(Resource):
    @jwt_required()
    def post(self, todo_id):
        """Assign this ToDo to the current user."""
        current_user = get_jwt_identity()
        result = mongo.db.todos.update_one(
            {'_id': ObjectId(todo_id)},
            {'$set': {
                'assignee': current_user,
                'updated_at': datetime.utcnow()
            }}
        )
        if result.matched_count == 0:
            api.abort(404, 'ToDo not found')
        
        # fetch the updated document
        doc = mongo.db.todos.find_one({'_id': ObjectId(todo_id)})
        # inject string id
        doc['id'] = str(doc['_id'])
        # remove raw ObjectId
        doc.pop('_id', None)

        return doc, 200
