from cvquery.main import db


class User(db.Model):

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        user_id = self.user_id
        users_posts = Post.query.filter_by(user_id = user_id)
        if users_posts is not None:
            for x in users_posts:
                x.delete()
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):

    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, user_id, post):
        self.user_id = user_id
        self.post = post

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()