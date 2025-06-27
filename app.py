from flask import Flask, render_template, redirect, url_for, request, flash
from flask_restx import Api
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                unset_jwt_cookies, create_access_token,
                                set_access_cookies)
from bson import ObjectId
from config import Config
from extensions import mongo, bcrypt, jwt
from resources.auth import api as auth_ns
from resources.user import api as user_ns
from resources.todo import api as todo_ns

app = Flask(__name__)
app.config.from_object(Config)

# init extensions
mongo.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Mount Swagger docs and API under /api
api = Api(app, title='Flask ToDo API', version='1.0', doc='/api', prefix='/api')
api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(todo_ns)

# UI Routes
@app.route('/')
@jwt_required(optional=True)
def index():
    if get_jwt_identity():
        return redirect(url_for('todos'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']))
            resp = redirect(url_for('todos'))
            set_access_cookies(resp, access_token)
            return resp
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    resp = redirect(url_for('login'))
    unset_jwt_cookies(resp)
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = dict(
            username=request.form['username'],
            email=request.form['email'],
            password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
            role='user'
        )
        mongo.db.users.insert_one(data)
        flash('User created, please login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'email': request.form['email']}})
        flash('Profile updated', 'success')
    return render_template('profile.html', user=user)

@app.route('/todos')
@jwt_required()
def todos():
    return render_template('todos.html')

@app.route('/todos/<id>')
@jwt_required()
def todo_detail(id):
    return render_template('todo_detail.html', todo_id=id)

@app.route('/epics')
@jwt_required()
def list_epics():
    return render_template('epics.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
