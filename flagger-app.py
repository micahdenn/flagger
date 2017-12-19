import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/')
def hello_world():
    image_name = "nail-and-gear.jpg"
    return render_template('index.html', variable = image_name)
       
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    image_name = file.filename

    file.save(f)
    
    #os.rename('static/' +str(image_name), 'flag.jpg')
    
    cmd = subprocess.check_output("python scripts/label_image.py \--image=static/" +str(image_name), shell=True)
    
    splitstr = cmd.split()
    rating = splitstr[4]
    if rating == 'bad':
        rating = 'Bad Flag'
    else:
        rating = 'Good Flag'
    
    confidence = 'Confidence: ' +str(splitstr[6])
    time = 'Evaluation Time: ' +str(splitstr[3])
    

    return render_template('index.html', variable = image_name, r = rating, c = confidence, t =time)

