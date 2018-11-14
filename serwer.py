from flask import Flask,render_template,url_for,flash, redirect
from forms import *
import datetime
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SwsEp2dnjOl4OlS2Bdux13OhwiJ288Wt'
logged = False

def getData():
	weight = 100
	data = str(datetime.datetime.utcnow())
	difrence = 0 - weight
	addresses = [{"MacAdress": "1234567890AB", "Name": "C1"}, {"MacAdress": "ABCDEF123456", "Name": "C2"}]
	num =2
	json_data=open("log.json").read()
	if(json_data):
		data = json.loads(json_data)
	json_data=open("last.json").read()
	if(json_data):
		new = json.loads(json_data)
		difrence = new['Weight'] - weight
		data['log'].append(new)
	with open('log.json', 'w') as outfile:
    		json.dump(data, outfile)
	data = {'Weight':weight,"Data":data,"Difrence":difrence, "MacAddresses":addresses,"Num":num}	
	with open('last.json', 'w') as outfile:
    		json.dump(data, outfile)

@app.route("/")
@app.route("/home")
def home():
	json_data=open("last.json").read()
	data = json.loads(json_data)
	return render_template('home.html',logged = logged,log = data)
@app.route("/about")
def about():
	return render_template('about.html',logged = logged)
@app.route("/devices")
def devices():
	json_data=open("config.json").read()
	data = json.loads(json_data)
	return render_template('devices.html',logged = logged,devices=data['Devices'])
@app.route("/logs")
def logs():
	return render_template('logs.html',logged = logged)

@app.route("/login",methods=["POST","GET"])
def login():
	form=loginform()
	if form.validate_on_submit():
		login = form.login.data
		password = form.password.data
		json_data=open("config.json").read()
		data = json.loads(json_data)
		if password == data["User"]["Password"] and login == data["User"]["Login"]:
			return redirect(url_for('home'))
		flash(u'Login lub haslo sa nieprawidlowe','warning')
	return render_template('login.html', form = form)

@app.route("/changeuserdata",methods=["POST","GET"])
def chpassword():
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
		return redirect(url_for('home'))
		flash(u'Data Changed','success')
	return render_template('chpassword.html', form=form)

@app.route("/addevice",methods=["POST","GET"])
def addevice():
	form = adddevice()
	if form.validate_on_submit():
		adresmac = form.adresmac.data
		name = form.name.data
		json_data=open("config.json").read()
		data = json.loads(json_data)
		data['Devices'].append({"MacAdress":adresmac,"Name":name})
		with open('config.json', 'w') as outfile:
    			json.dump(data, outfile)
		return redirect(url_for('home'))
		flash(u'Device added','success')
	return render_template('adddevice.html', form=form)

@app.route("/deldevice",methods=["POST","GET"])
@app.route("/deldevice/<mac>",methods=["POST","GET"])
def deldevice(mac):
	json_data=open("config.json").read()
	data = json.loads(json_data)
	data['Devices'][:]=[device for device in data['Devices'] if device.get('MacAdress')!=mac]
	with open('config.json', 'w') as outfile:
    		json.dump(data, outfile)
	flash(u'Device Deleted','success')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)


