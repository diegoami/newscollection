import re
from datetime import date, timedelta
from urllib.parse import urlparse, unquote, urlsplit
import yaml
import logging
import sys

def extract_date_str(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
        if index >= len(arrs):
            return None
    year, month, day = arrs[index], arrs[index + 1], arrs[index + 2]
    date_str = day + '-' + month + '-' + year

    return date_str

def extract_tags(tags):
    tag_base = [x.split('/')[-1] if len(x.split('/')[-1]) > 0 else x.split('/')[-2] for x in
                tags]
    return tag_base

def conv_to_date(str_date):
    try:
        return date(*(map(int, str_date.split('-'))))
    except:
        return None

def conv_From_(str_date):
    try:
        return date(*(map(int, str_date.split('-'))))
    except:
        return None


def extract_start_url( url):
    start_url = str(urlparse(url)[0])+'://'+str(urlparse(url)[1])+'/'
    return start_url


def extract_source( url):
    source = str(urlparse(url)[1]).upper()
    return source

def extract_source_without_www( url):
    try:
        source = extract_source( url).upper()
        all_parts = source.split('.')
        parts = [ x for x in all_parts if x not in['COM', 'WWW', 'UK', 'NET', 'ORG', 'CO']]
        return "".join(parts)
    except:
        return url


def extract_date(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
        if (index >= len(arrs)):
            return None
    if (all([arrs[index].isdigit(), arrs[index + 1].isdigit(), arrs[index + 2].isdigit()])):
        year, month, day = map(int, (arrs[index], arrs[index + 1], arrs[index + 2]))
    #date_str = day + '-' + month + '-' + year
        return date(year, month, day)
    else:
        return None

def extract_last_part(url):
    usplt = url.split('/')
    if (len(usplt) > 0):
        name = usplt[-1] if len(usplt[-1]) > 0 else usplt[-2]
        return unquote(name)
    else:
        return url

def extract_normpath( url):
    urlpart = urlsplit(url)
    url_result = urlpart.scheme +'://'+urlpart.netloc  +urlpart.path
    return url_result


def extract_host( url, with_http=True):
    urlparts = urlparse(url)
    if (len(urlparts)) >= 2:
        source = str(urlparts[0])+'://'+ str(urlparts[1])
        return source if with_http else urlparts[1]
    else:
        return None

def remove_emojis(text):
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)

    text = re_pattern .sub('', text)
    return text


def daterange(start_date, end_date, days_diff=1):
    if start_date <= end_date:
        for n1, n2 in zip(range((end_date - start_date).days + 1),range(1+days_diff, (end_date - start_date).days + 1+days_diff)):
            yield start_date + timedelta(n1), start_date + timedelta(n2)
    else:
        raise(ValueError)


def load_config(argv):
    config_file = sys.argv[1] if (len(sys.argv) > 1) else 'config.yml'
    logging.info("Loading {}".format(config_file))
    config = yaml.safe_load(open(config_file))
    return config
