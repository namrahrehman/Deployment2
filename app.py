# -*- coding: utf-8 -*-
"""
@author: Namrah Rehman
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash, url_for
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref 
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img 
from tensorflow.keras.preprocessing import image
import time
from tensorflow.keras import applications 
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

vgg16 = applications.VGG16(include_top=False, weights='imagenet')
#model = load_model('models/testModel.h5')

UPLOAD_FOLDER = './flask app/assets/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Create Database if it doesnt exist

app = Flask(__name__,static_url_path='/assets',
            static_folder='./flask app/assets', 
            template_folder='./flask app')
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
##############Database MODEL###############################

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
  
    def __repr__(self):
         return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

admin= Admin(app)
admin.add_view(ModelView(User, db.session))



class Radiologist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    licenseId = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return '<Radiologist %r>' % self.username


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img = db.Column(db.String(80), unique=True, nullable=False)
    Atelectasis = db.Column(db.String(80), unique=True, nullable=False)
    Cardiomegaly = db.Column(db.String(80), unique=True, nullable=False)
    Consolidation = db.Column(db.String(80), unique=True, nullable=False)
    EnlargedCardiomediastinum = db.Column(db.String(80), unique=True, nullable=False)
    Fracture = db.Column(db.String(80), unique=True, nullable=False)
    LungLesion = db.Column(db.String(80), unique=True, nullable=False)
    NoFinding = db.Column(db.String(80), unique=True, nullable=False)
    Pneumonia = db.Column(db.String(80), unique=True, nullable=False)
    Pneumothorax = db.Column(db.String(80), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Prediction %r>' % self.username

class Verified(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    img = db.Column(db.String(80), unique=True, nullable=False)
    Atelectasis = db.Column(db.String(80), unique=True, nullable=False)
    Cardiomegaly = db.Column(db.String(80), unique=True, nullable=False)
    Consolidation = db.Column(db.String(80), unique=True, nullable=False)
    EnlargedCardiomediastinum = db.Column(db.String(80), unique=True, nullable=False)
    Fracture = db.Column(db.String(80), unique=True, nullable=False)
    LungLesion = db.Column(db.String(80), unique=True, nullable=False)
    NoFinding = db.Column(db.String(80), unique=True, nullable=False)
    Pneumonia = db.Column(db.String(80), unique=True, nullable=False)
    Pneumothorax = db.Column(db.String(80), unique=True, nullable=False)
    

    def __repr__(self):
        return '<Verified %r>' % self.username
######################################################################
admin.add_view(ModelView(Radiologist, db.session))
admin.add_view(ModelView(Prediction, db.session))
admin.add_view(ModelView(Verified, db.session))
######################################################################

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    choice_switcher = RadioField('Choice?', validators=[InputRequired()], choices=[('choice1', 'Yes'), ], default='choice1')

# def save_img(file_path):
#    pic = load_img(file_path, target_size=(224, 224)) 
#    filename = secure_filename(pic.filename)
#    mimetype = pic.mimetype
#    img = Img(img=pic.read(), name=filename, mimetype=mimetype)
#    db.session.add(img)
#    db.session.commit()
#    return 

@app.route('/')
def root():
   return render_template('index.html')

@app.route('/index.html')
def index():
   return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
   return render_template('login.html', form=form)

@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
   form = RegisterForm()
   if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'


   return render_template('signup.html', form=form)

@app.route('/radio.html')
def displat_all():
   pred = Prediction.query.all()
   return render_template('radio.html', pred=pred)

@app.route('/contact.html')
def contact():
   return render_template('contact.html')

@app.route('/news.html')
def news():
   return render_template('news.html')

@app.route('/about.html')
def about():
   return render_template('about.html')

@app.route('/faqs.html')
def faqs():
   return render_template('faqs.html')

@app.route('/prevention.html')
def prevention():
   return render_template('prevention.html')

@app.route('/upload.html')
def upload():
   return render_template('upload.html')

@app.route('/upload_chest.html')
def upload_chest():
   return render_template('upload_chest.html')


@app.route('/uploaded_chest', methods = ['POST', 'GET'])
def uploaded_chest():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print("THIS IS FILE NAME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

   model = load_model('models/testModel.h5')

   #file_path1='./flask app/assets/images/upload_chest.jpg'
   filepath='./flask app/assets/images/'
   file_path=filepath+filename
   print("[INFO] loading and preprocessing image…") 
   image = load_img(file_path, target_size=(224, 224)) 
   image = img_to_array(image) 
   image = np.expand_dims(image, axis=0)
   image /= 255. 

   # save_img(file_path)
   
   bt_prediction = vgg16.predict(image) 
   preds = model.predict(bt_prediction)
   c1=str('%.2f' % (preds[0][0]*100))
   c2=str('%.2f' % (preds[0][1]*100))
   c3=str('%.2f' % (preds[0][2]*100))
   c4=str('%.2f' % (preds[0][3]*100))
   c5=str('%.2f' % (preds[0][4]*100))
   c6=str('%.2f' % (preds[0][5]*100))
   c7=str('%.2f' % (preds[0][6]*100))
   c8=str('%.2f' % (preds[0][7]*100))
   c9=str('%.2f' % (preds[0][8]*100))
   print(c1,c2,c3,c4,c5,c6,c7,c8,c9)

   new_prediction = Prediction(img=file_path, Atelectasis=c1 ,Cardiomegaly=c2,Consolidation=c3,EnlargedCardiomediastinum=c4,Fracture=c5,LungLesion=c6,NoFinding=c7,Pneumonia=c8, Pneumothorax=c9)
   db.session.add(new_prediction)
   db.session.commit()

   return render_template('results_chest.html', c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9)




@app.route('/dashboard.html')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.secret_key = ".."
   app.run()