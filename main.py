import os

from ShazamAPI import Shazam
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
basedir = os.path.abspath(os.path.dirname(__file__))

def testKazaam():
    mp3_file_content_to_recognize = open('uploads/Time Alone.mp3', 'rb').read()

    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    print(next(recognize_generator))  # current offset & shazam response to recognize requests

# gets the name of an audio file and prints out song info
def kazaam(filename):
    mp3_file_content_to_recognize = open('uploads/Time Alone.mp3', 'rb').read()

    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    print(next(recognize_generator))  # current offset & shazam response to recognize requests

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH= os.path.join(basedir, 'uploads'),
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000)

dropzone = Dropzone(app)
@app.route('/',methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'],f.filename))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
