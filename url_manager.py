from urllib.parse import urlparse, urlunparse
import os

KNOWN_PHISHING_FILE_PATH = 'known_phishing_urls.txt'
NOT_PHISHING_FILE_PATH = 'not_phishing_urls.txt'

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))
    return normalized_url

def load_urls(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            urls = f.read().splitlines()
            return set(urls)
    return set()

def add_url(file_path, url):
    with open(file_path, 'a') as f:
        f.write(f"{url}\n")

def check_known_phishing(url):
    normalized_url = normalize_url(url)
    return normalized_url in known_phishing_urls

def add_known_phishing(url):
    normalized_url = normalize_url(url)
    if normalized_url not in known_phishing_urls:
        known_phishing_urls.add(normalized_url)
        add_url(KNOWN_PHISHING_FILE_PATH, normalized_url)
        print(f"Added {normalized_url} to known phishing URLs.")
    else:
        print(f"{normalized_url} is already in the known phishing URLs.")

def check_not_phishing(url):
    normalized_url = normalize_url(url)
    return normalized_url in not_phishing_urls

def add_not_phishing_url(url):
    normalized_url = normalize_url(url)
    if normalized_url not in not_phishing_urls:
        not_phishing_urls.add(normalized_url)
        add_url(NOT_PHISHING_FILE_PATH, normalized_url)
        print(f"Added {normalized_url} to not phishing URLs.")
    else:
        print(f"{normalized_url} is already in the not phishing URLs.")

# Load known phishing and not phishing URLs from files
known_phishing_urls = load_urls(KNOWN_PHISHING_FILE_PATH)
not_phishing_urls = load_urls(NOT_PHISHING_FILE_PATH)
