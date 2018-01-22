import os
from FintechExplorerProject.settings import BASE_DIR

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'static/Manage/client_secret.json')
APPLICATION_NAME = 'Drive API Python Quickstart'

ColumbiaFintechFolderID = "0B5LDkXIhbPvyUktJcl91bEJ6SHM"



def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
    return credentials

def TruncateName(name_str):
    letter_limit = 50
    if (len(name_str) > letter_limit):
        return name_str[:letter_limit] + "..."
    else:
        return name_str

def SearchFolders(service, ParentFolderID):
    list_out = []
    page_token = None
    while True:
        response = service.files().list(q="'" + ParentFolderID + "' in parents and mimeType = 'application/vnd.google-apps.folder'",
            orderBy='modifiedTime desc', spaces='drive', fields='nextPageToken, files(id, name, webViewLink)', pageToken=page_token).execute()
        for file in response.get('files', []):
            list_out.append({'id':file.get('id'),'name':TruncateName(file.get('name')),'webLink':file.get('webViewLink')})
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return list_out

def SearchFiles(service, ParentFolderID, NameQuery, ContentQuery):
    list_out = []
    page_token = None
    while True:
        response = service.files().list(q="'"+ParentFolderID+"' in parents and name contains '"+NameQuery+"' and fullText contains '"+ContentQuery+"'",
            spaces='drive', fields='nextPageToken, files(id, name, webViewLink, thumbnailLink)', pageToken=page_token).execute()
        for file in response.get('files', []):
            list_out.append({'id':file.get('id'),'name':TruncateName(file.get('name')),'webLink':file.get('webViewLink'),'thumbLink':file.get('thumbnailLink')})
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return list_out