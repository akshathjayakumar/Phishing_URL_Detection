import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Loading dataset
urldata = pd.read_csv("feature_data.csv")

# Check if "Unnamed: 0" column exists and drop it
if "Unnamed: 0" in urldata.columns:
    urldata.drop("Unnamed: 0", axis=1, inplace=True)

# Displaying the first 10 rows
print(urldata.head(10))

# Displaying info about the dataset
print(urldata.info())

# Displaying value counts of the 'result' column
print(urldata["result"].value_counts())

# Plotting the count of URLs
plt.figure(figsize=(13,5))
sns.countplot(x='result', data=urldata)
plt.title("Count Of URLs", fontsize=20)
plt.xlabel("Type Of URLs", fontsize=18)
plt.ylabel("Number Of URLs", fontsize=18)
plt.show()

# Correlation heatmap
corrmat = urldata.corr()
f, ax = plt.subplots(figsize=(25,19))
sns.heatmap(corrmat, square=True, annot=True, annot_kws={'size':10})

# Setting plot sizes
from matplotlib import rcParams
rcParams['figure.figsize'] = 15,10

# Check available columns
print("Available columns:", urldata.columns)

# Plotting distributions
hist_features = ["url_length", "hostname_length", "fd_length"]  # Remove 'path_length' if not present

for feature in hist_features:
    if feature in urldata.columns:
        sns.histplot(data=urldata, x=feature, bins=100, hue='result')
        plt.xlabel(feature, fontsize=18)
        plt.ylabel("Number Of URLs", fontsize=18)
        plt.xlim(0, 150)
        plt.show()
    else:
        print(f"Feature '{feature}' not found in DataFrame")

# Removing unnecessary columns
urldata.drop(["label"], axis=1, inplace=True)

# Displaying the first few rows
print(urldata.head())

# Independent Variables
x = urldata[['hostname_length', 'url_length', 'fd_length', 'count_-', 'count_@', 'count_?', 'count_%', 'count_.', 'count_=', 'count_http', 'count_https', 'count_www', 'count_digits', 'count_letters', 'count_dir', 'use_of_ip']]

# Dependent Variable
y = urldata['result']

# Displaying x
print(x.head())

# Displaying y
print(y.head())

# Oversampling using SMOTE
from imblearn.over_sampling import SMOTE

x_sample, y_sample = SMOTE().fit_resample(x, y)

x_sample = pd.DataFrame(x_sample, columns=x.columns)
y_sample = pd.DataFrame(y_sample, columns=['result'])

# Checking the sizes of the sample data
print("Size of x-sample:", x_sample.shape)
print("Size of y-sample:", y_sample.shape)

# Data splitting
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x_sample, y_sample, test_size=0.2)
print("Shape of x_train:", x_train.shape)
print("Shape of x_test:", x_test.shape)
print("Shape of y_train:", y_train.shape)
print("Shape of y_test:", y_test.shape)

# Model definition


model = Sequential([
    Dense(64, activation='relu', input_shape=(x_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compiling the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training the model
history = model.fit(x_train, y_train, epochs=30, batch_size=64, validation_data=(x_test, y_test), verbose=1)

# Evaluating the model
loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
print('Test Loss:', loss)
print('Test Accuracy:', accuracy)

# Saving the model
model.save('phishing_model.h5')

# Displaying model training history
# Accuracy
plt.figure(figsize=(20,8))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

# Loss
plt.figure(figsize=(20,8))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
