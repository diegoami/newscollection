from urllib.parse import urlparse, unquote
from datetime import date
import re



def extract_date_str(url):
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


def extract_date(url):
    arrs = str(urlparse(url)[2]).split('/')
    index = 0
    while not arrs[index].isdigit():
        index += 1
    year, month, day = map(int, (arrs[index], arrs[index + 1], arrs[index + 2]))
    #date_str = day + '-' + month + '-' + year
    return date(year, month, day)

def extract_last_part(url):
    usplt = url.split('/')
    if (len(usplt) > 0):
        name = usplt[-1] if len(usplt[-1]) > 0 else usplt[-2]
        return unquote(name)
    else:
        return url



def extract_host( url):
    urlparts = urlparse(url)
    source = str(urlparts[0])+'://'+ str(urlparts[1])
    return source

def remove_emojis(text):
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)

    text = re_pattern .sub('', text)
    return text