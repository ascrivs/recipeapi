from app import db, login_manager
import datetime
from flask import current_app, abort
from flask_login import UserMixin, AnonymousUserMixin, current_user
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
import os







recipe_history = db.Table('recipe_history',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)


recipe_tags = db.Table(
    'recipe_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)



class User(UserMixin, db.Model):

    __tablename__ = 'users'
    
    default_photo = 'default.png'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(128),default=default_photo)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    pass_hash = db.Column(db.String(256), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    failed_pwd = db.Column(db.Integer, default=0)
    account_locked = db.Column(db.Boolean, default=False)
    role = db.Column(db.Integer, default=1)
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    user_recipe_history = db.relationship('Recipe', lazy='subquery', secondary=recipe_history, backref=db.backref('users', lazy=True) )
    

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        max_lockout = 3
        if not check_password_hash(self.pass_hash, password):
            if self.failed_pwd < max_lockout:
                 self.failed_pwd += 1
                 db.session.add(self)
                 db.session.commit()
            if self.failed_pwd >= max_lockout:
                self.account_locked = True
                db.session.add(self)
                db.session.commit()
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return f'User account: {self.username}.'

    def generate_confirmation_token(self, expiration=3600):
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        payload = {'confirm': self.id,
                    'exp': int(exp.timestamp())
                }
        token = jwt.encode(payload,current_app.config['SECRET_KEY'],algorithm='HS256')
        return token

    def confirm(self, token):
        try:
            data = jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False

        if data.get('confirm') != self.id or data.get('exp') < int(datetime.datetime.utcnow().timestamp()):
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    def ping(self):
        self.last_seen = datetime.datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String(32), default='recipe_default.png')
    tags = db.relationship('Tag', secondary=recipe_tags, back_populates='recipes')

    def __repr__(self):
        return f'{self.name}'



class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    recipes = db.relationship('Recipe', secondary=recipe_tags, back_populates='tags')

    def __repr__(self):
        return f'{self.name}'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(256))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipes = db.relationship('Recipe', backref='ingredients')

    def __repr__(self):
        return f'{self.details}'

class Direction(db.Model):
    __tablename__ = 'directions'

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.Text, default='Someone should really add some instructions here...')
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipes = db.relationship('Recipe', backref='directions')