from urllib.parse import urlparse
from datetime import date


def extract_date(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
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

def extract_source( url):
    source = str(urlparse(url)[1]).upper()
    return source


def conv_to_date(str_date):
    try:
        return date(*(map(int, str_date.split('-'))))
    except:
        return None