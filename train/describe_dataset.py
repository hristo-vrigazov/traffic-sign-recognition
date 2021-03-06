from load_dataset import load_dataset
import cv2

X_train, y_train, X_test, y_test = load_dataset()

n_train = len(X_train)

n_test = len(X_test)

image_shape = X_train[0].shape

n_classes = len(set(y_train))

print("Number of training examples =", n_train)
print("Number of testing examples =", n_test)
print("Image data shape =", image_shape)
print("Number of classes =", n_classes)

image = X_train[10]
print(image)

(B, G, R) = cv2.split(image)

cv2.imshow("Red", R)
cv2.waitKey(0)
cv2.imshow("Green", G)
cv2.waitKey(0)
cv2.imshow("Blue", B)
cv2.waitKey(0)

cv2.imshow('Training example', image)
cv2.waitKey(0)