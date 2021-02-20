import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import tensorflow.keras as keras
import librosa
import math
import numpy as np

app = Flask(__name__)
model = keras.models.load_model('models/cnn_model_80acc_130.h5')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=["POST"])
def upload():
    # extract filestorage object from request
    data = request.files['audioFile']
    
    # extract mfccs
    input = create_mfcc(data)
    # add additional dimension for color
    input = input[..., np.newaxis]

    # get prediction/confidences from model
    confidences = model.predict(input)

    # average the confidence for all segments
    averaged = np.mean(confidences, axis=0)
    averaged = averaged.tolist()

    return jsonify(confidences=averaged)

# loads song and extracts mfcc data.  Reshapes data to correct size for model
def create_mfcc(data, hop_length=512, n_fft=2048, sr=22050, n_mfcc=13, model_seg_size=130):
    mfcc_list = []

    # process audio files
    signal, sr = librosa.load(data, sr=sr)

    # extract mfcc feature data
    mfcc = librosa.feature.mfcc(signal,
                                sr=sr,
                                n_fft=n_fft,
                                n_mfcc=n_mfcc,
                                hop_length=hop_length)

    # transpose the mfcc data
    mfcc = mfcc.T

    # get number of rows
    num_rows = mfcc.shape[0]

    # calculate the maximum number of full segments we can slice
    max_segments = num_rows // model_seg_size
    maximum_rows = max_segments * model_seg_size

    # delete rows that dont add up to full segment
    mfcc = np.delete(mfcc, slice(maximum_rows-1, -1), 0)

    # reshape to 3-D array expected by model
    mfcc = np.reshape(mfcc, (-1, model_seg_size, n_mfcc))

    return mfcc


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)