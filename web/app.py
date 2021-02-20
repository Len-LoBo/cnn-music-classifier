import os
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import tensorflow.keras as keras
import librosa
import math
import numpy as np

app = Flask(__name__)
our_model = keras.models.load_model('models/cnn_model_6_segs_per_track.h5')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/upload', methods=["POST"])
def upload():

    print("request.files")
    data = request.files['audioFile']
    
    print("Calling create_mfcc")
    input = create_mfcc(data)
    input = input[..., np.newaxis]

    print("Calling predictions")
    prediction = predict(our_model, input)

    averaged = getAverageConfidences(prediction)
    averaged = averaged.tolist()
    print(averaged)

    return jsonify(confidences=averaged)


def create_mfcc(data, hop_length=512, n_fft=2048, sr=22050, n_mfcc=13, seg_size=216):
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

    num_rows = mfcc.shape[0]

    full_rows = num_rows // seg_size
    maximum_rows = full_rows * seg_size
    mfcc = np.delete(mfcc, slice(maximum_rows-1, -1), 0)
    mfcc = np.reshape(mfcc, (-1, seg_size, n_mfcc))
    return mfcc



def predict(model, X):
    # add a dimension to input data for sample - model.predict() expects a 4d array in this case

    # perform prediction
    print("Predicting")
    confidences = model.predict(X)

    print("Returning model")
    return confidences

def getAverageConfidences(confidences):
    avg_confidences = np.mean(confidences, axis=0)
    return avg_confidences

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)