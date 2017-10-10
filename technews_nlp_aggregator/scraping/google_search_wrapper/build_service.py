from apiclient.discovery import build

def create_google_service(developerKey):
    return build('customsearch', 'v1', developerKey=developerKey)