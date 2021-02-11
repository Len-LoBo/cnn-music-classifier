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
    input_file = create_mfcc(data)

    input_file = input_file[..., np.newaxis]
    
    print("Calling predictions")
    prediction = predict(our_model, input_file)
    return jsonify(predictions=prediction)


def create_mfcc(data, num_segments=6, hop_length=512, n_fft=2048, sample_rate=22050, num_mfcc=13):
    # arrays to hold calculated mfccs and mapped number
    mfccs = []
    labels = []

    samples_per_track = sample_rate * 30  # track duration = 30s
    samples_per_segment = int(samples_per_track / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    signal, sr = librosa.core.load(data, sr=sample_rate)

    # extract MFCCs
    for s in range(num_segments):
        # calculate start and finish sample for current segment
        start = samples_per_segment * s
        finish = start + samples_per_segment
        # extract mfcc
        mfcc = librosa.feature.mfcc(signal[start:finish], sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft,
                                    hop_length=hop_length)
        # transpose to correct dimensions
        mfcc = mfcc.T
        if len(mfcc) == num_mfcc_vectors_per_segment:
            return mfcc


def predict(model, X):
    # add a dimension to input data for sample - model.predict() expects a 4d array in this case

    print("Adding new axis")
    X = X[np.newaxis, ...]  # array shape (1 <- number of samples, 130, 13, 1)

    # perform prediction
    print("Predicting")
    print(X.shape)
    prediction = model.predict(X)

    prediction = prediction.tolist()

    print("Returning model")
    return prediction

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)