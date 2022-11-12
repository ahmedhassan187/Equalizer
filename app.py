from flask import Flask,render_template,request,send_from_directory
from flask_cors import CORS
from librosa import load
import os
from werkzeug.utils import secure_filename
from logic import logic
import numpy as np
import soundfile
from IPython.display import Audio
app = Flask(__name__)
CORS(app)
UPLOADS_FOLDER = './static'
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
@app.route("/")
def default():
    pass
@app.route("/upload",methods=['GET','POST'])
def upload():
    if (request.method == 'POST'):
        if "file" not in request.files:
            return {"there is an error":'err'},400
        file = request.files["file"]
        signal,sr = load(file)
        f_signal,freqs = logic.fourier(signal,sr)
        list_of_f = logic.select_range(freqs,100,10000,True)
        signal_rec = np.fft.irfft(logic.modify_magnitude(list_of_f,f_signal,0.0))
        completeName = os.path.join(app.config['UPLOADS_FOLDER'],'modified.mp3')
        completeName_2 = os.path.join(app.config['UPLOADS_FOLDER'],'signal.mp3')
        soundfile.write(completeName,signal_rec,sr)
        soundfile.write(completeName_2,signal,sr)
        return("hello")
@app.route('/static/<path:filename>')
def send_attachment(filename):
  return send_from_directory(app.config['UPLOADS_FOLDER'], 
    filename=filename)
@app.route('/sliders',methods=['GET','POST'])
def get_sliders_values():
    if (request.method == 'POST'):
        if "array" not in request.form:
            return {"there is an error":'err'},400
        array = request.form["array"]
        signal,sr = load('./static/signal.mp3')
        my_list = array.split(",")
        slider_list = [int(i) for i in my_list]
        f_signal,freqs = logic.fourier(signal,sr)
        list_f = logic.mode_1_ranges(sr)
        re_fou = logic.final_func(f_signal,freqs,list_f,slider_list)
        re_con = np.fft.irfft(re_fou)
        completeName = os.path.join(app.config['UPLOADS_FOLDER'],'modified.mp3')
        soundfile.write(completeName,re_con,sr)
        return "hello"
if __name__ == "__main__":
    app.run(debug=True,port='8080',host='0.0.0.0')
    