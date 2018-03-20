from flask import render_template,redirect,url_for,flash
from . import game

@game.route('/box',methods=['GET'])
def box():
	return render_template('game/box/index.html')
	
	