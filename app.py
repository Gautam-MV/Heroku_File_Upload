import os
from main import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,Response
from werkzeug.utils import secure_filename
import cv2

from camera import VideoCamera

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_video():		    
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	else:
		filename = secure_filename(file.filename)
		print(os.path.join(app.config['UPLOAD_FOLDER']))
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_video filename: ' + filename)
		flash('Video successfully uploaded and displayed below')
        #return render_template('upload.html', filename=filename)
		return Response(gen(VideoCamera(filename)),mimetype='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/display/<filename>')
def display_video(filename):
    cap = cv2.VideoCapture(f'static/uploads/{filename}.mp4')
    while True:
        _, img = cap.read()
        cv2.imshow('Image', img)
        key = cv2.waitKey(1)
        if key==27:
            break

    cap.release()
    cv2.destroyAllWindows()
	#print('display_video filename: ' + filename)
	
    #return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()

