from app import app,db,loginmanager
from flask import render_template,redirect,request,flash,url_for
from app.models import User,Device
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_user,logout_user,login_required
from datetime import date
import string
import secrets
import os
import smtplib
from flask_mail import Mail, Message
import flask_excel as excel


mail_config = {
    "MAIL_SERVER": 'smtp.office365.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": "kamaujay@outlook.com",
    "MAIL_PASSWORD": "JahKam123?" 
}


app.config.update(mail_config)
mail = Mail(app)


UPLOAD_FOLDER = 'app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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



#function to save device images
def save_device_img(device_image):
    random_hex = secrets.token_hex(8)
    _, f_text = os.path.splitext(device_image.filename)
    picture_fn = random_hex + f_text
    picture_path = os.path.join(app.root_path, 'static/deviceimg', picture_fn)
    device_image.save(picture_path)
    return picture_fn


#book repair route
@app.route('/book_repair',methods=['GET','POST'])
@login_required
def book_repair():
    if request.method == 'POST':
        if request.files:
            alphabet = string.ascii_letters + string.digits
            device_key = ''.join(secrets.choice(alphabet) for i in range(32))
            name=request.form['device_name']
            model=request.form['model']
            fault=request.form['fault']
            image = request.files['device_image']
            device_image = save_device_img(image)
            user_id=current_user.id
            device=Device(name=name,model=model,fault=fault,user_id=user_id,device_key=device_key, device_image=device_image)
            db.session.add(device)
            db.session.commit()

            flash('device booked successfully')
            return redirect(url_for('index'))

    return render_template('booking_repair.html')


@app.route('/view_device/<dvk>',methods=['GET','POST'])
@login_required
def view_device(dvk):
    device=Device.query.filter_by(device_key=dvk).first()
    device_image = url_for('static', filename='deviceimg/' + device.device_image)
    return render_template('view_device.html',device=device, device_image=device_image)


#tecnicin page
@app.route('/technician/<usk>',methods=['GET','POST'])
@login_required
def technician(usk):
    devices=Device.query.all()
    for device in devices:
        device.device_image = url_for('static', filename='deviceimg/' + device.device_image)

    return render_template('tech3.html',devices= devices)


@app.route('/start_repair/<dvk>')
def start_repair(dvk):
    device=Device.query.filter_by(device_key=dvk).first()
    if device.status=='booked':
        device.status="under repair"
        db.session.commit()
    return redirect(url_for('view_device',dvk=device.device_key))


@app.route('/end_repair/<dvk>',methods=['GET','POST'])
@login_required
def end_repair(dvk):

    device=Device.query.filter_by(device_key=dvk).first()
    email=device.user.email
   
    if request.method=='POST':
        device.tech_resolution=request.form['tech_resolution']
        device.repair_price= request.form['repair_price']
        device.status='repair complete'
        db.session.add(device)
        db.session.commit()
        recipients =[email]
       
        body= f"{device.status} {device.tech_resolution} at a cost of {device.repair_price} \n kindly make payment via 0796199724"
        message = Message(body=body, recipients=recipients, sender='kamaujay@outlook.com')
        mail.send(message)
    return redirect(url_for('view_device',dvk=dvk))



@app.route("/export", methods=['GET'])
def export():
    query_sets= Device.query.all()
    column_names = ['id', 'name']
    return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")
    return redirect(url_for('home'))


@app.route('/delete_device/<dvk>')
@login_required
def delete_device(dvk):
    device = Device.query.filter_by(device_key=dvk).first()
    db.session.delete(device)
    return redirect(url_for('index'))


@app.route('/make_technician/<usk>')
@login_required
def make_technician(usk):
    user=User.query.filter_by(user_key=usk)
    user.is_tecnician=1
    db.session.add(user)
    return redirect(url_for('index'))




@app.route('/admin/<usk>')
@login_required
def admin(usk):
    return render_template('admin.html')













#logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))  