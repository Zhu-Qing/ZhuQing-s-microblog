from flask_wtf import Form
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField('猜猜我的名字？',validators=[Required()])
	submit = SubmitField('提交')
	
class PostForm(Form):
	body = TextAreaField('你想说说什么？',validators=[Required()])
	submit = SubmitField('提交')
	
