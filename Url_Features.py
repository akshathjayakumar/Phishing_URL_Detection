import re
from urllib.parse import urlparse


def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0


def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits


def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')


def having_ip_address(url):
    match = re.search(
        # IPv4 in hexadecimal
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return -1
    else:
        return 1



def hostname_length(url):
    return len(urlparse(url).netloc)

def url_length(url):
    return len(urlparse(url).path)


def get_counts(url):

    count_features = []

    i = url.count('-')
    count_features.append(i)

    i = url.count('@')
    count_features.append(i)

    i = url.count('?')
    count_features.append(i)

    i = url.count('%')
    count_features.append(i)

    i = url.count('.')
    count_features.append(i)

    i = url.count('=')
    count_features.append(i)

    i = url.count('http')
    count_features.append(i)

    i = url.count('https')
    count_features.append(i)

    i = url.count('www')
    count_features.append(i)

    return count_features


