# Load pickled data
import pickle
import os.path
import os
import wget

import zipfile

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

def load_dataset():
	training_file = 'train.p'
	testing_file = 'test.p'

	if not os.path.isfile(training_file) or not ps.path.isfile(testing_file):
		url = 'https://d17h27t6h515a5.cloudfront.net/topher/2016/November/581faac4_traffic-signs-data/traffic-signs-data.zip'
		filename = wget.download(url)
		unzip(filename, '.')
		os.remove(filename)

	with open(training_file, mode='rb') as f:
	    train = pickle.load(f)
	with open(testing_file, mode='rb') as f:
	    test = pickle.load(f)

	X_train, y_train = train['features'], train['labels']
	X_test, y_test = test['features'], test['labels']

	return X_train, y_train, X_test, y_test