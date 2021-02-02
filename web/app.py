from flask import Flask, jsonify, request, render_template
import tensorflow as tf
import numpy as np
import librosa

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
        # Currently, memory growth needs to be the same across GPUs
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
        except RuntimeError as e:
            # Memory growth must be set before GPUs have been initialized
            print(e)

    audio_file = request.files['audioFile']

    # convert audio file to mfcc data
    mfcc = save_mfcc(audio_file)

    # add last dimension to data (model expects this)
    mfcc = mfcc[..., np.newaxis]

    # run prediction using model
    predictions = predict('cnn_model_77acc_lr15.h5', mfcc)

    return jsonify(predictions=predictions)


# runs prediction on model
def predict(model_name, X):

    # loads the model -- probably should happen outside this function
    model = tf.keras.models.load_model('models/' + model_name)

    # add 3rd dimension for the model (essentially says its just one data input)
    X = X[np.newaxis, ...]

    # returns values at all output neurons as np array
    predictions = model.predict(X)

    predictions = predictions.tolist()

    return predictions


# converts audio file to mfcc data
def save_mfcc(audio_path,
            sr=22050,
            n_mfcc=13,
            n_fft=2048,
            hop_length=512):

    # process files
    signal, sr = librosa.load(audio_path, sr=sr)

    # store mfcc
    mfcc = librosa.feature.mfcc(signal,
                                sr=sr,
                                n_fft=n_fft,
                                n_mfcc=n_mfcc,
                                hop_length=hop_length)

    # transpose the mfcc data, and slice it to the right size (130, 13)
    # TODO: I think it might be best to repeatedly slice it and take an average at the end?
    mfcc = mfcc.T
    mfcc = mfcc[:130]
    return mfcc


    
if __name__ == "__main__":
    app.run(port=5001)