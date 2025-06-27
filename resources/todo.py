from flask_restx import Namespace, Resource, fields, reqparse
from flask import request
from extensions import mongo
from bson.objectid import ObjectId
from datetime import datetime

api = Namespace('todo', description='ToDo operations')

todo_model = api.model('Todo', {
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
        mongo.db.todos.insert_one(data)
        data['id'] = str(data.get('_id', data['key']))
        return data, 201

    @api.expect(parser)
    @api.marshal_with(todo_model, as_list=True)
    def get(self):
        args = parser.parse_args()
        todos = list(mongo.db.todos.find()
                     .skip((args['page']-1)*args['per_page'])
                     .limit(args['per_page']))
        for t in todos:
            t['id'] = str(t['_id'])
        return todos

@api.route('/<string:id>')
class TodoResource(Resource):
    @api.marshal_with(todo_model)
    def get(self, id):
        t = mongo.db.todos.find_one({'_id': ObjectId(id)})
        if not t: api.abort(404)
        t['id'] = str(t['_id'])
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