import flask_sqlalchemy
import psycopg2
import configparser
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import manager

db = SQLAlchemy()

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.id

    @property
    def is_authenticated(self):
        return True

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    @manager.user_loader
    def load_user(id):
        return User.query.get(id)


class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.has_role('admin'))

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login/')


class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.has_role('admin')):
            return redirect(url_for('login'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        logout_user()
        return redirect(url_for('/'))


class Connect_to_db():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.conf')

    def connect(self):
        user = self.config.get('DATABASE', 'USERNAME')
        password = self.config.get('DATABASE', 'PASSWORD')
        host = self.config.get('DATABASE', 'HOST')
        dbname = self.config.get('DATABASE', 'DBNAME')
        port = self.config.get('DATABASE', 'PORT')
        print(host)
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        return conn

    def create_table(self):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS "User" (id SERIAL PRIMARY KEY, username varchar, password varchar, token varchar)""")
                conn.commit()
