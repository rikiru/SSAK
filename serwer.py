from flask import Flask,render_template,url_for,flash, redirect,session
from forms import *
from mythread import writeDataToLog,checkWeight
import threading
import time
import datetime
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SwsEp2dnjOl4OlS2Bdux13OhwiJ288Wt'
curentData = {}




@app.route("/")
@app.route("/home")
def home():	
	if not 'logged' in session:
		return redirect(url_for('login'))
	global curentData
	logged = session['logged']
	json_data=open("last.json").read()
	data = json.loads(json_data)
	return render_template('home.html',logged = logged,log = data,refresh = True) 
@app.route("/about")
def about():	
	if not 'logged' in session:
		return redirect(url_for('login'))
	logged = session['logged']
	return render_template('about.html',logged = logged)
@app.route("/devices")
def devices():
	if not 'logged' in session:
		return redirect(url_for('login'))
	logged = session['logged']
	json_data=open("config.json").read()
	data = json.loads(json_data)
	return render_template('devices.html',logged = logged,devices=data['Devices'])
@app.route("/logs")
def logs():	
	if not 'logged' in session:
		return redirect(url_for('login'))
	logged = session['logged']
	json_data=open("log.json").read()
	data = json.loads(json_data)
	return render_template('logs.html',logged = logged,logs = data)

@app.route("/login",methods=["POST","GET"])
def login():
	logged = False
	form=loginform()
	if form.validate_on_submit():
		login = form.login.data
		password = form.password.data
		json_data=open("config.json").read()
		data = json.loads(json_data)
		if password == data["User"]["Password"] and login == data["User"]["Login"]:
			session['logged'] = True
			return redirect(url_for('home'))
		flash(u'Login lub haslo sa nieprawidlowe','warning')
	return render_template('login.html', form = form , logged = logged)

@app.route("/logout",methods=["POST","GET"])
def logout():
	session.pop('logged', None)
   	return redirect(url_for('login'))

@app.route("/changeuserdata",methods=["POST","GET"])
def chpassword():
	if not 'logged' in session:
		return redirect(url_for('login'))
	logged = session['logged']
	form = changeform()
	if form.validate_on_submit():
		newlogin = form.username.data
		newpassword = form.newpassword.data
		json_data=open("config.json").read()
		data = json.loads(json_data)
		data["User"]["Login"] = newlogin
		data["User"]["Password"] = newpassword
		with open('config.json', 'w') as outfile:
    			json.dump(data, outfile)
		flash(u'Data Changed','success')
		return redirect(url_for('home'))
	return render_template('chpassword.html', form=form,logged = logged)

@app.route("/addevice",methods=["POST","GET"])
def addevice():
	if not 'logged' in session:
		return redirect(url_for('login'))
	logged = session['logged']
	form = adddevice()
	if form.validate_on_submit():
		adresmac = form.adresmac.data
		name = form.name.data
		json_data=open("config.json").read()
		data = json.loads(json_data)
		data['Devices'].append({"MacAdress":adresmac,"Name":name})
		with open('config.json', 'w') as outfile:
    			json.dump(data, outfile)
		flash(u'Device added','success')
		return redirect(url_for('home'))
	return render_template('adddevice.html', form=form,logged = logged)

@app.route("/deldevice",methods=["POST","GET"])
@app.route("/deldevice/<mac>",methods=["POST","GET"])
def deldevice(mac):
	if not 'logged' in session:
		return redirect(url_for('login'))
	json_data=open("config.json").read()
	data = json.loads(json_data)
	data['Devices'][:]=[device for device in data['Devices'] if device.get('MacAdress')!=mac]
	with open('config.json', 'w') as outfile:
    		json.dump(data, outfile)
	flash(u'Device Deleted','success')
	return redirect(url_for('devices'))

if __name__ == '__main__':
	checkWeight()
	app.run(debug=True)


