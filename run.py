from cvquery.main import app, api
from cvquery.api import UserView, PostView, UserPostsView

api.add_resource(UserView, '/api/users')
api.add_resource(PostView, '/api/posts')
api.add_resource(UserPostsView, '/api/user/<username>/posts')

app.run(host='0.0.0.0', debug=True)