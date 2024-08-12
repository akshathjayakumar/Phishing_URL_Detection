import pandas as pd
from Url_Features import *

def extract_features(url):
    url_features = []

    url_features.append(hostname_length(url))    # hostname length
    url_features.append(url_length(url))         # URL length
    url_features.append(fd_length(url))          # FD length
    url_features += get_counts(url)              # Special characters count
    url_features.append(digit_count(url))        # Digit count
    url_features.append(letter_count(url))       # Letter count
    url_features.append(no_of_dir(url))          # Number of directories
    url_features.append(having_ip_address(url))  # Presence of IP address

    return url_features

# Load the dataset
urldata = pd.read_csv("/Users/akshathjayakumar/artificialintelligenceprojects/Phishing_URL_Detection/urldata.csv")

# Extract features for each URL
features_list = urldata['url'].apply(extract_features)
features_df = pd.DataFrame(features_list.tolist(), columns=[
    'hostname_length', 'url_length', 'fd_length', 'count_-', 'count_@', 'count_?', 'count_%',
    'count_.', 'count_=', 'count_http', 'count_https', 'count_www', 'count_digits',
    'count_letters', 'count_dir', 'use_of_ip'
])

# Add labels and result to the features DataFrame
features_df['label'] = urldata['label']
features_df['result'] = urldata['result']

# Save the feature data to a new CSV file
features_df.to_csv("/Users/akshathjayakumar/artificialintelligenceprojects/Phishing_URL_Detection/feature_data.csv", index=False)

print(features_df.head())
