# Load pickled data
import pickle
import os.path
import os
import wget
import cv2
import zipfile
import numpy as np


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        for member in zf.infolist():
            # Path traversal defense copied from
            # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
            words = member.filename.split('/')
            path = dest_dir
            for word in words[:-1]:
                while True:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if not drive:
                        break
                if word in (os.curdir, os.pardir, ''):
                    continue
                path = os.path.join(path, word)
            zf.extract(member, path)


def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def load_grayscale():
    X_train, y_train, X_test, y_test = load_dataset()

    X_train = np.array([grayscale(img) for img in X_train]).reshape(-1,32,32,1)
    X_test = np.array([grayscale(img) for img in X_test]).reshape(-1,32,32,1)

    return X_train, y_train, X_test, y_test

def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b


def load_dataset():
    training_file = 'train.p'
    testing_file = 'test.p'

    if not os.path.isfile(training_file) or not os.path.isfile(testing_file):
        url = 'https://d17h27t6h515a5.cloudfront.net/topher/2016/November/581faac4_traffic-signs-data/traffic-signs-data.zip'
        filename = wget.download(url)
        unzip(filename, '.')
        os.remove(filename)

    with open(training_file, mode='rb') as f:
        train = pickle.load(f)
    with open(testing_file, mode='rb') as f:
        test = pickle.load(f)

    validation_test_limit = int(len(test['features']) * 9.0 / 10.0)
    X_train, y_train = train['features'], train['labels']
    X_test, y_test = test['features'], test['labels']
    
    del train
    del test

    X_train, y_train = shuffle_in_unison(X_train, y_train)
    X_test, y_test = shuffle_in_unison(X_test, y_test)

    return X_train, y_train, X_test, y_test