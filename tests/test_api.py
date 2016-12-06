from cvquery.main import db, app, api
from cvquery.models import User, Post
import pdb
import codecs
import json
from flask import jsonify
from cvquery.api import UserView, PostView, UserPostsView
from base64 import b64encode



api.add_resource(UserView, '/api/users')
api.add_resource(PostView, '/api/posts')
api.add_resource(UserPostsView, '/api/user/<username>/posts')



db.drop_all()
db.create_all()

app.testing = True
client = app.test_client()

reader = codecs.getreader("utf-8")

#provjerava jesu li dodana 3 korisnika, mirko, darko, slavko
def test_user_post():
    response1 = client.post("/api/users", data=json.dumps(dict(username='mirko', password='mirkova_lozinka')),content_type='application/json')
    response2 = client.post("/api/users", data=json.dumps(dict(username='darko', password='darkova_lozinka')),content_type='application/json')
    response3 = client.post("/api/users", data=json.dumps(dict(username='slavko', password='slavkova_lozinka')),content_type='application/json')

    assert response1.status == '200 OK'
    assert response2.status == '200 OK'
    assert response3.status == '200 OK'

#provjerava jesu li ta 3 korisnika izlistana
def test_user_get():
    response = client.get("/api/users")
    #loads decoding json
    str_response = response.get_data(as_text=True)
    data = json.loads(str_response)

    assert len(data)==3
    assert 'mirko' in str_response
    assert 'darko' in str_response
    assert 'slavko' in str_response



#provjerava mogu li useri staviti postove
def test_post_post():
    response1 = user_posts('mirko', 'mirkova_lozinka', 'mirkov prvi post')
    response2 = user_posts('mirko', 'mirkova_lozinka', 'mirkov drugi post')
    response3 = user_posts('darko', 'darkova_lozinka', 'darkov prvi post')
    response4 = user_posts('slavko', 'slavkova_lozinka', 'slavkov prvi post')

    assert '200 OK' in response1.status
    assert '200 OK' in response2.status
    assert '200 OK' in response3.status
    assert '200 OK' in response4.status


def user_posts(username, password, post):
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'

    response = client.post("/api/posts", data=json.dumps(dict(post= post)) , headers=headers)
    return response



#provjerava jesu li svi napisani postovi izlistani
def test_post_get():
    response = client.get("/api/posts")
    str_response = response.get_data(as_text=True)
    data = json.loads(str_response)

    assert len(data)==4
    assert 'mirkov prvi' in str_response
    assert 'mirkov drugi' in str_response
    assert 'darkov prvi' in str_response
    assert 'slavkov prvi' in str_response

    
#provjerava da mirko ne moze izbrisati darka
def test_user_delete_fail():
    username = 'mirko'
    password = 'mirkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    response = client.delete("/api/users", data=json.dumps(dict(user_id=2)) , headers=headers)
    assert "\"success\": false" in response.get_data(as_text=True)

#provjerava moze li darko izbrisati sebe (i svoje postove)
def test_user_delete_success():
    username = 'darko'
    password = 'darkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.delete("/api/users", data=json.dumps(dict(user_id=2)), headers=headers)
    assert "\"success\": true" in response.get_data(as_text=True)

    response = client.get("/api/posts")
    str_response = response.get_data(as_text=True)
    data = json.loads(str_response)

    assert len(data)==3
    assert 'darkov' not in str_response


#provjerava da mirko ne moze izbrisati slavkov post
def test_post_delete_fail():
    username = 'mirko'
    password = 'mirkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.delete("/api/posts", data=json.dumps(dict(post_id=4)) , headers=headers)
    assert "\"success\": false" in response.get_data(as_text=True)

#provjerava da slavko moze izbrisati svoj post
def test_post_delete_success():
    username = 'slavko'
    password = 'slavkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.delete("/api/posts", data=json.dumps(dict(post_id=4)), headers=headers)
    assert "\"success\": true" in response.get_data(as_text=True)

#provjerava da slavko ne moze promijeniti mirkov post
def test_post_put_fail():
    username = 'slavko'
    password = 'slavkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.delete("/api/posts", data=json.dumps(dict(post_id=1, post = 'slavko ne moze promijeniti mirkov')) , headers=headers)
    assert "\"success\": false" in response.get_data(as_text=True)

#provjerava da mirko moze promijeniti svoj post
def test_post_put_success():
    username = 'mirko'
    password = 'mirkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.put("/api/posts", data=json.dumps(dict(post_id=1, post = 'mirko promijenio prvi post')) , headers=headers)
    assert "\"success\": true" in response.get_data(as_text=True)

#provjerava user posts view
def test_userposts_get():
    response = client.get("/api/user/mirko/posts")
    str_response = response.get_data(as_text=True)
    data = json.loads(str_response)

    assert len(data)==2
    assert 'promijenio' in str_response
    assert 'mirkov drugi' in str_response

#provjerava user update
def test_user_update():
    username = 'mirko'
    password = 'mirkova_lozinka'
    headers = {}
    headers['Authorization'] = 'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
    headers['Content-Type'] = 'application/json'
    
    response = client.put("/api/users", data=json.dumps(dict(user_id=1, new_username = 'mirkooooo')) , headers=headers)
    assert "\"success\": true" in response.get_data(as_text=True)

