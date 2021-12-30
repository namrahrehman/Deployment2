# -*- coding: utf-8 -*-
"""
@author: Namrah Rehman
"""

from flask import Flask, render_template, request, session, redirect, url_for, flash, url_for
import os
from flask_bootstrap import Bootstrap

from werkzeug.security import generate_password_hash, check_password_hash


from datetime import datetime
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img 
from tensorflow.keras.preprocessing import image
import time
from tensorflow.keras import applications 


vgg16 = applications.VGG16(include_top=False, weights='imagenet')
#model = load_model('models/testModel.h5')

UPLOAD_FOLDER = './flask app/assets/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Create Database if it doesnt exist

app = Flask(__name__,static_url_path='/assets',
            static_folder='./flask app/assets', 
            template_folder='./flask app')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)


##############Database MODEL###############################

######################################################################

######################################################################



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

   
   return render_template('results_chest.html', c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, c7=c7, c8=c8, c9=c9)




@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')



if __name__ == '__main__':
   app.secret_key = ".."
   app.run()
