1. In order to run the application, run app.py
2. Make sure that path are mentioned correctly
3. Replace with your API for fetching more URL information from whois.

Adjust the threshold value. I have given the value as 30.5 in the app.py. False positives and negatives
can occur.

Details of the code:

1. train.py

This code provides a complete workflow for analyzing and modeling a dataset of URLs, focusing on distinguishing between
phishing and legitimate URLs. The process begins with importing necessary libraries like pandas for data manipulation,
matplotlib and seaborn for visualization, and tensorflow for building the deep learning model.

Dataset Loading and Cleaning:

The dataset is loaded from a CSV file, and any irrelevant columns, such as "Unnamed: 0," are removed to ensure the data is
clean and ready for analysis.
Initial exploratory data analysis (EDA) is performed by displaying the first few rows of the dataset and providing a summary
of its structure with the info() method. This includes checking the distribution of the target variable (result), which
indicates whether a URL is phishing or not.

Data Visualization:

The script includes visualizations to understand the dataset better. A count plot of the different types of URLs (result) is
generated to show the balance or imbalance between classes. A correlation heatmap is also created to reveal relationships
between various features, helping to identify which features might be more relevant for the model.

Feature Engineering and Data Preparation:

The dataset is further prepared by extracting key features related to URL characteristics, such as URL length, hostname
length, and the presence of specific characters. This is essential for the machine learning model to understand the patterns
that might indicate phishing behavior.
To address class imbalance, the code uses SMOTE (Synthetic Minority Over-sampling Technique), a technique to oversample the
minority class, ensuring the model has enough data to learn from.

Model Building and Training:

A neural network model is constructed using TensorFlow's Keras API. The model consists of several dense layers, with ReLU
activations for intermediate layers and a sigmoid activation for the output layer, making it suitable for binary
classification.

The model is compiled with the Adam optimizer and binary crossentropy loss, then trained on the prepared dataset.
The training process is monitored using validation data to avoid overfitting.

Model Evaluation and Saving:

After training, the model's performance is evaluated on the test data, providing metrics like accuracy and loss.
These metrics are also visualized using plots to give insights into how well the model has learned.
Finally, the trained model is saved as an .h5 file, making it easy to deploy for future predictions.


2. url_predictor.py

This code snippet defines a function get_prediction that uses a pre-trained deep learning model to predict the probability
of a given URL being malicious. The function starts by loading the deep learning model from a specified .h5 file path
using TensorFlow Keras. It then extracts features from the input URL using an external extract_features function.
These features are fed into the model to obtain a prediction, which represents the probability of the URL being malicious.
This probability is converted to a percentage, rounded to three decimal places, and returned. This function is designed for
real-time URL classification using a deep learning approach.

3. url_manager.py

This code snippet manages lists of known phishing and non-phishing URLs with functionalities for normalization, storage,
and verification. It defines several functions:

normalize_url(url): Normalizes a URL by parsing and reassembling it to ensure consistency.
load_urls(file_path): Loads URLs from a specified file into a set, creating an empty set if the file doesn’t exist.
add_url(file_path, url): Appends a URL to a specified file.
check_known_phishing(url): Checks if a given URL is in the set of known phishing URLs.
add_known_phishing(url): Adds a URL to the known phishing URLs if it isn’t already present and updates the file.
check_not_phishing(url): Checks if a given URL is in the set of known non-phishing URLs.
add_not_phishing_url(url): Adds a URL to the non-phishing URLs if it isn’t already present and updates the file

4. Url_Features.py

This code snippet provides functions for extracting various features from URLs, which can be used for tasks such as URL
classification. Here’s a brief overview of each function:

fd_length(url): Computes the length of the first directory in the URL's path. Returns 0 if the URL path is empty or doesn't
contain directories.

digit_count(url): Counts the number of numeric characters in the URL.

letter_count(url): Counts the number of alphabetic characters in the URL.

no_of_dir(url): Counts the number of directories (segments) in the URL path, based on the number of slashes (/).

having_ip_address(url): Checks if the URL contains an IP address (IPv4 or IPv6). Returns -1 if an IP address is found,
1 otherwise.

hostname_length(url): Returns the length of the hostname in the URL.

url_length(url): Returns the length of the URL path.

get_counts(url): Counts the occurrences of specific characters and substrings in the URL (-, @, ?, %, ., =, http, https, www).
Returns these counts as a list.

5. prediction.py

This code snippet defines a function get_prediction that makes predictions on a URL using a pre-trained deep learning model.
Here’s a summary of its functionality:

Load the Model: It loads a deep learning model from the specified path using load_model. Ensure that you have the correct
path for your model file.

Prepare Features: It calls a function prepare_features(url) to extract and format the features from the URL that will be
input to the model. This function needs to be defined elsewhere in your code.

Predict: It uses the model to make a prediction based on the prepared features. The prediction value is printed for debugging
purposes.

Validate Prediction: It checks if the prediction is in the range [0, 1]. If not, it raises an error indicating that the
prediction is out of range.

Return Prediction: It returns the prediction value.

6. Feature_Extractor.py

The extract_features function processes a URL to extract a set of numerical features used for model input. Here's a breakdown of its functionality:

Initialize Feature List: An empty list, url_features, is created to store the extracted features.

Extract Features:

Hostname Length: The length of the hostname is appended to url_features.
Path Length: The length of the URL path is added.
First Directory Length: The length of the first directory in the path is included.
Character Counts: Counts of specific characters and substrings are extracted using get_counts(url) and added to the
feature list.
Digit Count: The number of digits in the URL is appended.
Letter Count: The number of letters in the URL is added.
Number of Directories: The count of directories in the URL path is appended.
IP Address Check: Indicates if the URL contains an IP address.
Return Features: The complete list of features is returned as a numerical representation suitable for input to a
machine learning model.

This function integrates various feature extraction methods to provide a comprehensive set of attributes for evaluating
the URL. Ensure that all functions used in extract_features (e.g., hostname_length, url_length, get_counts, etc.) are
correctly implemented and imported from Url_Features.

7. feature_extraction.py

This code snippet processes a dataset of URLs to extract features and prepare it for analysis or modeling. Here's a
summary of its functionality:

Feature Extraction: The extract_features function collects various attributes from each URL, including hostname length,
URL length, length of the first directory, counts of special characters, digit count, letter count, number of directories, and the presence of an IP address.

Load Dataset: It reads the URL dataset from a CSV file into a DataFrame using pandas.

Apply Feature Extraction: It applies the extract_features function to each URL in the dataset and creates a new DataFrame
with these features.

Add Labels: The labels and results from the original dataset are added to the new DataFrame.

Save Processed Data: The DataFrame containing the features and labels is saved to a new CSV file for further use.

Preview Data: It prints the first few rows of the processed DataFrame to verify the results.

8. app.py

This code snippet sets up a Flask web application to handle URL analysis and management tasks. Here's an overview of its functionality:

Imports: Includes necessary libraries and modules for web development, HTTP requests, and URL feature extraction.

App Initialization: Creates a Flask app instance.

Model Path: Specifies the path to the pre-trained model used for URL prediction.

Short URL Services: Defines a list of known URL shortening services to check if a URL is a short URL.

URL Expansion: Includes functions to expand shortened URLs and fetch WHOIS information for a domain.

Routes:

/: Renders the homepage.
/predict: Handles URL predictions. It checks if the URL is a short URL and expands it if needed, checks known phishing
lists, and uses the model to predict if the URL is suspicious.
/mark_phish: Marks a URL as phishing and updates the known phishing list.
/mark_not_phish: Marks a URL as not phishing and updates the known non-phishing list.
/more_info: Fetches and returns WHOIS information for a URL.
Error Handling and Debugging: Includes print statements for debugging and error handling to provide feedback on URL
processing and prediction.

Run the App: Starts the Flask app on 0.0.0.0 and port 5017, enabling debugging mode.

This application provides a web interface for URL analysis, allowing users to classify URLs, manage known phishing and
non-phishing URLs, and retrieve additional domain information.






