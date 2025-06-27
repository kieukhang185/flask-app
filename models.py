from datetime import datetime

class User:
    def __init__(self, data):
        self.id = str(data.get('_id') or data.get('id'))
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.role = data.get('role', 'user')

class Todo:
    def __init__(self, data):
        self.id = data.get('id')
        self.key = data.get('key')
        self.title = data['title']
        self.description = data.get('description', '')
        self.status = data.get('status', 'new')
        self.label = data.get('label', '')
        self.reporter = data['reporter']
        self.assignee = data.get('assignee')
        self.type = data['type']
        self.epic = data.get('epic')  # optional epic id
        self.parent_task = data.get('parent_task')  # optional parent task id for sub-tasks
        self.comments = data.get('comments', [])
        self.created_at = data.get('created_at', datetime.utcnow())
        self.updated_at = data.get('updated_at', datetime.utcnow())
