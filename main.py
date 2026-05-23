import os
import time

import torch
from flask import Flask, request, jsonify, send_file
from transformers import AutoProcessor, pipeline

from model import WhisperLargeV3
from tools import data_to_srt
from api import variable_controls,format_converter,save_data
######################################  import AI Model
WhisperModel=WhisperLargeV3()



app = Flask(__name__)



@app.route('/', methods=['POST',"GET"])
def main():
    return jsonify({"status": "True", "message": "APİ Aktf"}), 200




@app.route('/subtitles', methods=['POST',"GET"])
def process_audio():
    # Dosya kontrolü
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "Dosya gönderilmedi"}), 400
        
    else:
        audio_file = request.files['file']
        audio_bytes = audio_file.read() # Ham bayt verisini al
    
        speech, sr = WhisperModel.Load_data(audio_bytes)

    variable_controls(WhisperModel,request.form)
    result=WhisperModel.preadiction(speech=speech, sr=sr)

    subtitle_path=format_converter(result,request.form)
    print(subtitle_path)
    return send_file(subtitle_path, as_attachment=True)

if __name__ == '__main__':
    # REST API 5000 portunda çalışır
    app.run(host='0.0.0.0', port=8888, debug=False)