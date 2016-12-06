from flask import jsonify, request, g
from flask_restful_swagger_2 import Resource, swagger
from flask_httpauth import HTTPBasicAuth
import json
from cvquery.models import User
from cvquery.models import Post
from cvquery.main import logger

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or user.password!=password:
        return False
    g.user = user
    return True


class UserView(Resource):

    @swagger.doc({
        'tags': ['user'],
        'description': 'Returns list of all users',
        'responses': {
            '200': {
                'description': 'Users',
            }
        }
    })
    def get(self):
        """Returns list of all users"""
        users = User.query.all()
        
        dicts = []
        for user in users:
            dicts.append({'username' : user.username})

        log_req('/users/', request)
        
        return jsonify(dicts)


    @swagger.doc({
        'tags': ['user'],
        'description': 'Creates a new user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'User',
            }
        },
      
    })
    def post(self):
        """Creates a new user"""
        username = request.json.get('username')
        password = request.json.get('password')

        if username is None or password is None:
            return jsonify({"error": "username or password blank"})
        if User.query.filter_by(username = username).first() is not None:
            return jsonify({"error": "username already exists"})

        user = User(username, password)
        user.save()

        log_req('/users/', request)

        return jsonify({"username": user.username, "success": True})

    @swagger.doc({
        'tags': ['user'],
        'description': 'Deletes an user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'User',
            }
        },
      
    })
    @auth.login_required
    def delete(self):
        """Deletes an user"""
        usr_id = request.json.get('user_id')
        success = False

        if(g.user.user_id == usr_id):
            User.query.filter_by(user_id = usr_id).first().delete()
            success = True

        log_req('/users/', request)

        return jsonify({"user_id": usr_id, "success": success})

    @swagger.doc({
        'tags': ['user'],
        'description': 'Updates an user',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'user',
            }
        },
      
    })
    @auth.login_required
    def put(self):
        """Updates an user"""
        user_id = request.json.get('user_id')
        new_username = request.json.get('new_username')
        new_password = request.json.get('new_password')
        success = False

        user = User.query.filter_by(user_id = user_id).first()

        if (g.user.user_id == user.user_id):
            if new_username is not None:
                user.username = new_username
            if new_password is not None:
                user.password = new_password
            user.save()
            success = True

        log_req('/users/', request)

        return jsonify({"user_id": user_id, "success": success})


class PostView(Resource):

    @swagger.doc({
        'tags': ['post'],
        'description': 'Returns list of all posts',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'Posts',
            }
        },
      
    })
    def get(self):
        """Returns list of all posts"""
        posts = Post.query.all()

        dicts = []
        for post in posts:
            dicts.append({'post' : post.post})

        log_req('/posts/', request)

        return jsonify(dicts)

    @swagger.doc({
        'tags': ['post'],
        'description': 'Creates a new post',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'post',
            }
        },
      
    })
    @auth.login_required
    def post(self):
        """Creates a new post"""
        post = request.json.get('post')
        user_id = g.user.user_id

        post = Post(user_id, post)
        post.save()

        log_req('/posts/', request)

        return jsonify({"user_id": user_id, "success": True})



    @swagger.doc({
        'tags': ['post'],
        'description': 'Delets a post',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'post',
            }
        },
      
    })
    @auth.login_required
    def delete(self):
        """Deletes a post"""
        post_id = request.json.get('post_id')
        success = False

        post = Post.query.filter_by(post_id = post_id).first()

        if (g.user.user_id == post.user_id):
            post.delete()
            success = True

        log_req('/posts/', request)

        return jsonify({"post_id": post_id, "success": success})

    @swagger.doc({
        'tags': ['post'],
        'description': 'Updates a post',
        'produces':[
            'application/json'
        ],
        'responses': {
            '200': {
                'description': 'post',
            }
        },
      
    })
    @auth.login_required
    def put(self):
        """Updates a post"""
        post_id = request.json.get('post_id')
        new_text = request.json.get('post')
        success = False

        post = Post.query.filter_by(post_id = post_id).first()

        if (g.user.user_id == post.user_id):
            post.post = new_text
            post.save()
            success = True

        log_req('/posts/', request)

        return jsonify({"post_id": post_id, "success": success})


class UserPostsView(Resource):

    @swagger.doc({
        'tags': ['user posts'],
        'description': 'Gets all posts of a user with username',
        'produces':[
            'application/json'
        ],
        'parameters':[{
            'name': 'username',
            'in': 'path',
            'type': 'string',
        }],
        'responses': {
            '200': {
                'description': 'User posts',
            }
        },
      
    })
    def get(self, username):
        """Gets all posts of a user with username"""
        user = User.query.filter_by(username = username).first()

        posts = Post.query.filter_by(user_id = user.user_id)
        posts = [post.post for post in posts]

        log_req('/user/'+user.username+'/posts', request)

        return jsonify({"posts": posts, "success": True})

def log_req(path, req):
    browser = req.user_agent.browser
    logger.info('/users/' + str(browser))
        