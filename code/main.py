import os
import logging
import sys
import filetype
import numpy as np
import tensorflow as tf
import librosa


def main():
    # suppress non-critical tensorflow logging to command line
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
    logging.getLogger('tensorflow').setLevel(logging.FATAL)

    # check for command line argument, and find its file type
    try:
        file_path = sys.argv[1]
        file_type = filetype.guess(file_path)

    # exception for missing command line argument
    except IndexError:
        print("You failed to provide audio file path as command line argument")
        sys.exit(1)

    # exception for file not found
    except FileNotFoundError:
        print("Could not find audio wav file.")
        sys.exit(1)

    # these functions show how to use filetype package
    # print('File extension: %s' % file_type.extension)
    # print('File MIME type: %s' % file_type.mime)

    # if audio file is correct type (wav)
    if file_type.mime == 'audio/x-wav':

        # convert audio file to mfcc data
        mfcc = save_mfcc(file_path)

        # add last dimension to data (model expects this)
        mfcc = mfcc[..., np.newaxis]

        # run prediction using model
        predictions = predict('my_model.h5', mfcc)

        # dictionary of labels
        label_dict = {
            0: 'Jazz',
            1: 'Reggae',
            2: 'Rock',
            3: 'Blues',
            4: 'Hiphop',
            5: 'Country',
            6: 'Metal',
            7: 'Classical',
            8: 'Disco',
            9: 'Pop'
        }

        # get index of highest prediction
        predicted_index = np.argmax(predictions, axis=1)[0]

        # get label of highest prediction
        predicted_label = label_dict[predicted_index]

        # soft and format confidence list
        result = zip(label_dict.values(), predictions[0].tolist())
        result = list(result)
        result.sort(key=lambda x: x[1], reverse=True)

        # print output
        print(f"Predicted Genre: {predicted_label}\n")
        print(f"Confidences:")
        for x, y in result:
            print(f'{x}: %{y*100:.2f}')

    # error if audio type is not correct type
    else:
        print("Audio file must be .wav")
        sys.exit(1)


# runs prediction on model
def predict(model_name, X):

    # loads the model -- probably should happen outside this function
    model = tf.keras.models.load_model('../models/' + model_name)

    # add 3rd dimension for the model (essentially says its just one data input)
    X = X[np.newaxis, ...]

    # returns values at all output neurons as np array
    predictions = model.predict(X)

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
    main()
