from urllib.parse import urlparse

def remove_query_part( url):
    o = urlparse( url)

    url_without_query_string = o.scheme + "://" + o.netloc + o.path
    return url_without_query_string


def url_to_filename(k):


    k = str.replace(k, '/', '_')
    k = str.replace(k, 'https:__', '')
    k = str.replace(k, 'http:__', '')
    k = str.replace(k, '.', '_')
    k = k +'.html'
    return k
