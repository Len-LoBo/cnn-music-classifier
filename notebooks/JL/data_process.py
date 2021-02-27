import os
import math
import numpy as np
import librosa


DATA_PATH = '../mai_project/wavfiles'


def main():
    # create numpy arrays from the mfccs created and the corresponding genre
    np_mfccs, np_genres = create_mfcc(DATA_PATH)
    # save multiple arrays into zipped archive npz file to be loaded for training/testing model
    np.savez(DATA_PATH + '/' + 'data.npz', mfccs=np_mfccs, genre=np_genres)


def create_mfcc(data_path, num_segments=5, hop_length=512, n_fft=2048, sample_rate=22050, num_mfcc=13):
    # arrays to hold calculated mfccs and mapped number
    mfccs = []
    labels = []

    samples_per_track = sample_rate*30  # track duration = 30s
    samples_per_segment = int(samples_per_track / num_segments)
    num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

    # mapping of genre to number
    genre_dict = {
        'jazz': 0,
        'reggae': 1,
        'rock': 2,
        'blues': 3,
        'hiphop': 4,
        'country': 5,
        'metal': 6,
        'classical': 7,
        'disco': 8,
        'pop': 9
    }

    # process each wav file in data set
    for file in os.listdir(DATA_PATH):
        if file.endswith('.wav'):
            print("Processing file " + file)
            filepath = data_path + '/' + file
            signal, sr = librosa.core.load(filepath, sr=sample_rate)

            # use genre filename to map number to MFCC for training
            label = str(file).split('.')[0]
            label_mapped = genre_dict[label]

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
                    mfccs.append(mfcc.tolist())
                    labels.append(label_mapped)

    # convert to numpy arrays for processing
    np_mfccs = np.array(mfccs)
    np_genres = np.array(labels)

    return np_mfccs, np_genres


if __name__ == '__main__':
    main()
