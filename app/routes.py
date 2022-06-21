from app import app,db,loginmanager
from flask import render_template,redirect,request,flash,url_for
from app.models import User,Device
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from datetime import date

loginmanager.login_view='login'

#register new user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username'])
        # if user:
        #     flash("username already taken")
        user=User(username=request.form['username'],email=request.form['email'],password=generate_password_hash(request.form['password']),is_admin=False,phone=request.form['phone'])
        db.session.add(user)
        db.session.commit()
        flash('registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')

#login user
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username']).first()
        if user:
            if check_password_hash(user.password,request.form['password']):
                login_user(user,remember=True)
                flash('login successful')
                return redirect(url_for('index'))
        flash('incorrect username or password')
        return redirect(url_for('login'))
    return render_template('login.html')

#route for welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')


#route for index
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
    return render_template('index.html')


#book repair route
@app.route('/book_repair',methods=['GET','POST'])
@login_required
def book_repair():
    if request.method == 'POST':
        name=request.form['device_name']
        model=request.form['model']
        fault=request.form['fault']
        user_id=current_user.id
        device=Device(name=name,model=model,fault=fault,user_id=user_id)
        db.session.add(device)
        db.session.commit()
        flash('device booked successfully')
        return redirect(url_for('index'))

    return render_template('booking_repair.html')




























#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))