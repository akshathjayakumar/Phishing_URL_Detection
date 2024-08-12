import requests
from flask import Flask, render_template, request, jsonify
from url_predictor import get_prediction  # Make sure this function is defined in your `url_predictor` module
from url_manager import normalize_url, check_known_phishing, add_known_phishing, check_not_phishing, add_not_phishing_url  # Ensure these functions are defined in your `url_manager` module

app = Flask(__name__)

# Path to the trained model
model_path = '/Users/akshathjayakumar/artificialintelligenceprojects/Phishing_URL_Detection/models/phishing_model.h5'

# List of known URL shortening services
short_url_services = [
    "bit.ly", "goo.gl", "t.co", "tinyurl.com", "ow.ly", "buff.ly", "adf.ly",
    "is.gd", "bit.do", "mcaf.ee", "soo.gd", "s2r.co", "clic.ru", "cutt.ly",
    "shorturl.at", "rb.gy", "short.io"
]

def is_short_url(url):
    # Check if the URL domain matches any known shortening services
    return any(service in url for service in short_url_services)

def expand_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Error expanding URL {url}: {e}")
        return None

def fetch_whois_info(api_key, domain):
    url = f"https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON"
    response = requests.get(url)
    data = response.json()
    whois_record = data.get('WhoisRecord', {})
    registry_data = whois_record.get('registryData', {}).get('rawText', '')
    lines = registry_data.strip().split('\n')
    parsed_data = {}
    for line in lines:
        key_value = line.strip().split(':', 1)
        if len(key_value) == 2:
            key = key_value[0].strip()
            value = key_value[1].strip()
            parsed_data[key] = value

    required_keys = [
        "Domain Name", "Registry Domain ID", "Updated Date", "Creation Date",
        "Registry Expiry Date", "Registrar", "Registrar IANA ID"
    ]

    result = ""
    for key in required_keys:
        result += f"{key}: {parsed_data.get(key, 'Not available')}<br>"
    return result

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    print(f"Checking URL: {url}")  # Debug output

    # Check if the URL is a short URL and expand it if necessary
    if is_short_url(url):
        print(f"Expanding short URL: {url}")  # Debug output
        expanded_url = expand_url(url)
        if expanded_url:
            url = expanded_url
            print(f"Expanded URL: {url}")  # Debug output
        else:
            return f"<h2>URL is not valid</h2>"

    # Automatically classify .gov and .gov.in URLs as Not Suspicious
    if url.endswith('.gov') or url.endswith('.gov.in') or url.endswith('gov.in/'):
        print(f"URL ends with .gov or .gov.in: {url}")  # Debug output
        return "<h2>Prediction: Not Suspicious</h2>"

    try:
        normalized_url = normalize_url(url)
        in_known_phishing = check_known_phishing(normalized_url)
        in_not_phishing = check_not_phishing(normalized_url)

        if in_known_phishing:
            result = "Suspicious"
            print(f"URL is in the known phishing list: {url}")  # Debug output
        elif in_not_phishing:
            result = "Not Suspicious"
            print(f"URL is in the not phishing list: {url}")  # Debug output
        else:
            prediction = get_prediction(url, model_path)
            print(f"Model Prediction: {prediction}")  # Debug output
            prediction_percentage = round(prediction)
            print(f"Prediction percentage: {prediction_percentage}")  # Debug output
            result = "Suspicious" if prediction_percentage > 30.5 else "Not Suspicious"
    except ValueError as e:
        result = f"Error: {str(e)}"
    return f"<h2>Prediction: {result}</h2>"

@app.route('/mark_phish', methods=['POST'])
def mark_phish():
    data = request.get_json()
    url = data.get('url', '').strip()
    print(f"Marking URL as phishing: {url}")  # Debug output
    if url:
        try:
            add_known_phishing(url)
            response = {'message': 'URL marked as phishing.'}
        except Exception as e:
            response = {'message': f'Error: {str(e)}'}
    else:
        response = {'message': 'No URL provided.'}
    return jsonify(response)

@app.route('/mark_not_phish', methods=['POST'])
def mark_not_phish():
    data = request.get_json()
    url = data.get('url', '').strip()
    print(f"Marking URL as not phishing: {url}")  # Debug output
    if url:
        try:
            add_not_phishing_url(url)
            response = {'message': 'URL marked as not phishing.'}
        except Exception as e:
            response = {'message': f'Error: {str(e)}'}
    else:
        response = {'message': 'No URL provided.'}
    return jsonify(response)

@app.route('/more_info', methods=['POST'])
def more_info():
    data = request.get_json()
    url = data.get('url', '').strip()
    print(f"Fetching WHOIS information for: {url}")  # Debug output
    if url:
        try:
            api_key = 'API Key'  # Replace with your API key
            whois_info = fetch_whois_info(api_key, url)
            return jsonify({'info': whois_info})
        except Exception as e:
            return jsonify({'info': f'Error: {str(e)}'})
    else:
        return jsonify({'info': 'No URL provided.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5017)
