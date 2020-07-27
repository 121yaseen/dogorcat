from flask import Flask, render_template, request, redirect, url_for
from keras.models import load_model
from keras.preprocessing import image
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
model=load_model('models/cat_and_dog_breed.hdf5')
inverted_classes = {0: '111', 1: '112', 2: '113', 3: '114', 4: '115', 5: '221', 6: '222', 7: '223', 8: '224', 9: '225'}
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def home():
  return render_template("index.html")
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        img = request.files['pic']
        filename = secure_filename(img.filename)
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filepath = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = image.load_img(path= filepath,target_size=(128,128,3))
        img = image.img_to_array(img)
        test_img = img.reshape((1,128,128,3))
        img_class = model.predict_classes(test_img)
        prediction_classes = [ inverted_classes.get(item,item) for item in img_class ]
        class_ = str(prediction_classes[0][0])
        breed = str(prediction_classes[0][1:]) #I just know the breed number, don't know the breed name
        if(class_ == '1'):
          class_ = "Hey, this is a  cat"
        if(class_ == '2'):
          class_ = "Hey, this is a  dog"
        breed = prediction_classes[0][1:]

        return render_template("result.html", prediction=class_, filepath = filepath)
@app.route('/<filename>')
def display_image(filename):
  return redirect(url_for('static', filename='uploads/' + filename), code=301)
if __name__ == "__main__":
  app.run()
