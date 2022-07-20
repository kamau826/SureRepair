from app import app,db,loginmanager
from flask import render_template,redirect,request,flash,url_for
from app.models import User,Device
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from datetime import date
import string
import secrets

loginmanager.login_view='login'

#register new user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        user=User.query.filter_by(username=request.form['username'])
        # if user:
        #     flash("username already taken")
        alphabet = string.ascii_letters + string.digits
        user_key = ''.join(secrets.choice(alphabet) for i in range(32))
        user=User(username=request.form['username'],email=request.form['email'],password=generate_password_hash(request.form['password']),
                   is_admin=False,phone=request.form['phone'],user_key=user_key)
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
    devices=Device.query.filter_by(user_id=current_user.id)
    return render_template('index.html',devices=devices)


#book repair route
@app.route('/book_repair',methods=['GET','POST'])
@login_required
def book_repair():
    if request.method == 'POST':
        alphabet = string.ascii_letters + string.digits
        device_key = ''.join(secrets.choice(alphabet) for i in range(32))
        name=request.form['device_name']
        model=request.form['model']
        fault=request.form['fault']
        user_id=current_user.id
        device=Device(name=name,model=model,fault=fault,user_id=user_id,device_key=device_key)
        db.session.add(device)
        db.session.commit()
        flash('device booked successfully')
        return redirect(url_for('index'))

    return render_template('booking_repair.html')


@app.route('/view_device/<dvk>',methods=['GET','POST'])
@login_required
def view_device(dvk):
    device=Device.query.filter_by(device_key=dvk)
    return render_template('view_device.html',device=device)

@app.route('/technician/<usk>',methods=['GET','POST'])
@login_required
def technician(usk):
    devices=Device.query.all()
    return render_template('technician.html',devices=devices)


@app.route('/start_repair/<int:id>')
def start_repair(id):
    device=Device.query.get(id)
    if device.status=='booked':
        device.status="under repair"
    else:
        device.status='repair complete'
    db.session.commit()
    return redirect(url_for('view_device',id=id))



























#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))