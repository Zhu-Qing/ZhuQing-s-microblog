from app import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class Permission:
	FOLLOW = 0X01
	COMMENT = 0X02
	WRITE_ARTICLES = 0X4
	MODERATE_COMMENTS = 0X08
	ADMINISTER = 0X80
	

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
class User(UserMixin,db.Model):
	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
		if self.role is None:
			self.role = Role.query.filter_by(default=True).first()
	
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64),unique=True, index=True)
	role_id = db.Column(db.Integer,db.ForeignKey('role.id'))
	role = db.relationship('Role',backref=db.backref('Users',lazy=True))
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post',backref=db.backref('author',lazy=True))
	
	def can(self, perm):
		return self.role is not None and self.role.has_permission(perm)
	
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	
	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)
		
	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return '<User %r>' % self.username

class Role(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	permissions = db.Column(db.Integer)
	default = db.Column(db.Boolean,default=False,index=True)
	#users = db.relationship('User',backref='role')
	
	def has_permission(self, perm):
		return self.permissions & perm == perm
	
	@staticmethod
	def remove_roles(*args):
		name = args
		print(args)
		print(len(args))
		for r in args:
			role = Role.query.filter_by(name=r).first()
			if role is not None:
				db.session.delete(role)
				print('Success to delete role %s in Role table.'% r)
			else:
				print('Role name %s is not exist in Role table.'% r)
				
		if len(args) is 0:
			print('Delete all roles in Role table.')
			for r in Role.query.all():
				db.session.delete(r)
				
		db.session.commit()
			
	
	@staticmethod
	def insert_roles():
		roles = {
			'User':(Permission.FOLLOW|
					Permission.COMMENT|
					Permission.WRITE_ARTICLES, True),
			'Administrator':(0xff,False)
			}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions=roles[r][0]
			role.default=roles[r][1]
			db.session.add(role)
		db.session.commit()
	
	def __repr__(self):
		return '<Role %r>' % self.name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))