from flask import Flask, render_template, request, redirect, url_for
from database import *
from flask import session as login_session

app = Flask(__name__)

def verify_password(email,password):
	user = session.query(user).filter_by(email=email).first()
	if not user or not user.verify_password(password):
		return False
	return True

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
	elif request.method =='POST':
		email= request.form['email']
		password= request.form ['password']
		if email is None or password is None:
			flash('Missing Arguments')
			return redirect(url_for('signin'))
		if verify_password(email,password):
			user=session.query(user).filter_by(email=email).one()
			flash('Login Successful,welcome,%s' % user.name)
			login_session['name']=user.name
			login_session['email']=user.email
			login_session['id']=user.id
			return redirect(url_for('signin'))
		else:
			flash('Incorrect username/password combination')
			return redirect(url_for('signin'))
	
@app.route('/signout')
def signgout():
	if 'id' not in login_session:
		flash('you msut be logged in order to log out ')
		return redirect(url_for('signin'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash('Logged Out Successfully')
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
