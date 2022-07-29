import os
import glob
import sqlite3
from ShazamAPI import Shazam
from flask import Flask, render_template, request
from flask_dropzone import Dropzone
basedir = os.path.abspath(os.path.dirname(__file__))

def testKazaam():
    mp3_file_content_to_recognize = open('uploads/Time Alone.mp3', 'rb').read()

    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()

    #print(next(recognize_generator))  # current offset & shazam response to recognize requests
    return next(recognize_generator)



# gets the name of an audio file and prints out song info
def kazaam():
    #get name of latest file in uploads to be recognized
    list_of_files = glob.glob('uploads/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    mp3_file_content_to_recognize = open(f'{latest_file}', 'rb').read()

    shazam = Shazam(mp3_file_content_to_recognize)
    recognize_generator = shazam.recognizeSong()
    return next(recognize_generator)  # current offset & shazam response to recognize requests



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




@app.route('/display', methods=['POST', 'GET'])
def display():
    
    generator = kazaam()

    song_title = generator[1]['track']['title']
 
    song_subtitle = generator[1]['track']['subtitle']
    
    #print list of tuples for song lyrics
    '''for item in generator[1]['track']['sections'][1]['text']:
      print(item)'''
    
    artist_photo = generator[1]['track']['images']['coverart']

    list = generator[1]['track']['sections'][1]['text']

    #create database and insert values
    connection = sqlite3.connect("site.db")
    cur = connection.cursor()
    

    cur.execute('''CREATE TABLE IF NOT EXISTS RecentSearches(
                          ID INT PRIMARY KEY,
                          SONGNAME TEXT,
                          ARTISTNAME TEXT
                          );''')

    
    cur.execute("INSERT INTO RecentSearches (SONGNAME) VALUES('{}, {}');".format(song_title, song_subtitle))

    connection.commit()

    cur.execute("SELECT SONGNAME FROM RecentSearches ORDER BY ID DESC LIMIT 5")
    list_of_recent = cur.fetchall()
    recent_five = list_of_recent
    print(recent_five)
    return render_template('display.html', Artist_Title = song_subtitle, Song_Title = song_title, list = list, len = len(list), 
        artist_photo = artist_photo, recent_five = recent_five, len_recent = len(recent_five))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
