from flask import Flask, render_template, request, redirect, url_for
from database import *

app = Flask(__name__)

@app.route('/')
def mainpage():
	horses = session.query(Horse).all()
	return render_template("mainpage.html", horses = horses)

@app.route('/aboutus')
def aboutus():
	return render_template("aboutus.html")


@app.route('/signin', methods=['GET','POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	else:
		new_email = request.form['email']
		new_password = request.form['password']

		users = session.query(Users).filter_by(email = new_email, password=new_password).all()
		if(len(users) == 0):
			return redirect(url_for('signin.html'))
		else:
			flask_session['user_email'] = new_email
	return render_template("signin.html")
	
@app.route('/signout')
def signgout():
	session.pop('user_id', None)
	return redirect(url_for('mainpage'))



@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html')
	else:
		new_name = request.form["fullname"]
		new_email = request.form["email"]
		new_age = request.form["age"]
		new_password = request.form["password"]

		new_user = Users(
			fullname=new_name,
			email=new_email,
			age= new_age, 
			password=new_password,
			)

		session.add(new_user)
		session.commit()
		return render_template("signup.html")



if __name__=='__main__':
	app.run(debug=True)
