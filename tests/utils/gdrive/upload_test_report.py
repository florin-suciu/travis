import time
from os import path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
JSON_LOCATION = 'tests/utils/gdrive'


def upload_file():
    """Uploads the test report to G Drive."""
    store = file.Storage(path.join(JSON_LOCATION, 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path.join(JSON_LOCATION, 'credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    folder_id = '0B8EKbFOBYbsLMVF0YUxvSEhuMGM'
    time_str = time.strftime("%Y-%m-%d-%H:%M:%S")
    file_metadata = {
        'name': 'report-{}.html'.format(time_str),
        'parents': [folder_id]
    }

    media = MediaFileUpload(path.join('reports', 'report.html'),
                            mimetype='text/html',
                            resumable=True)
    up_file = service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id').execute()
    download_link = 'https://drive.google.com/uc?id={}&export=download'.format(up_file.get('id'))
    print(download_link)


if __name__ == '__main__':
    upload_file()
