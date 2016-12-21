from load_dataset import load_train_test_val

X_train, y_train, X_test, y_test, X_val, y_val = load_train_test_val()

print(('Number of classes in training dataset: {}'.format(len(set(y_train)))))
print('Number of classes in test dataset: {}'.format(len(set(y_test))))
print('Number of classes in val dataset: {}'.format(len(set(y_val))))

print(X_val[0])