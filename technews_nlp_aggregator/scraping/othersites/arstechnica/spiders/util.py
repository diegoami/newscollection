from urllib.parse import urlparse, unquote
from datetime import date, datetime, timedelta
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



def end_condition(date):
    if not date:
        return False
    #if date.month < 10 or date.day < 28:
    if date.year < 2017:
        return True
    else:
        return False