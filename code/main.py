import os
import logging
import sys
import filetype
import numpy as np
import librosa

# this silencing tensorflow logging output
# needs to go before import for...reasons
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
import tensorflow as tf


def main():

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

        print("\nPredicting...\n")

        # convert audio file to mfcc data
        mfcc_list = save_mfcc(file_path)

        # song is split up into segements
        # below code takes average of confidences from all segements
        combined_prediction = [0.] * 10
        for mfcc in mfcc_list:
            mfcc = mfcc[..., np.newaxis]
            prediction = predict('cnn_model_77acc_lr15.h5', mfcc)
            for index in range(10):
                combined_prediction[index] += prediction[0][index]

        # take average by dividing each confidence by the number of predictions
        for c in range(len(combined_prediction)):
            combined_prediction[c] /= len(mfcc_list)

        # genre labels mapped to integers
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

        # get index of highest confidence prediction
        predicted_index = combined_prediction.index(max(combined_prediction))

        # get label of highest confidence prediction
        predicted_label = label_dict[predicted_index]

        # sort and format confidences list
        result = zip(label_dict.values(), combined_prediction)
        result = list(result)
        result.sort(key=lambda x: x[1], reverse=True)

        # print output
        print('=================================')
        print(f"Predicted Genre: {predicted_label}\n")
        print('=================================')
        print(f"Confidences:")
        print('=================================')
        for x, y in result:
            print(f'{x}: %{y*100:.2f}')

    # error if audio type is not correct type
    else:
        print("Audio file must be .wav")
        sys.exit(1)


# runs prediction on model
def predict(model_name, X):

    # loads the model -- probably should happen outside this function
    model = tf.keras.models.load_model('models/' + model_name)

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

    mfcc_list = []

    # process audio files
    signal, sr = librosa.load(audio_path, sr=sr)

    # extract mfcc feature data
    mfcc = librosa.feature.mfcc(signal,
                                sr=sr,
                                n_fft=n_fft,
                                n_mfcc=n_mfcc,
                                hop_length=hop_length)

    # transpose the mfcc data
    mfcc = mfcc.T

    # model expects (1, 130, 13, 1) sized data
    # therefore full song must be split into segments of mfcc data
    # store all segments in list of mfcc data (130 in length)
    for x in range(0, len(mfcc), 130):
        temp_mfcc = mfcc[x:x+130]
        if len(temp_mfcc) == 130:
            mfcc_list.append(temp_mfcc)
    return mfcc_list


if __name__ == "__main__":
    main()
