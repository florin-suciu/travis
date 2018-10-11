import argparse
from os import path

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.file'
JSON_LOCATION = 'tests/utils/gdrive'
FOLDER_ID = '0B8EKbFOBYbsLMVF0YUxvSEhuMGM'


def upload_file(file_path):
    """Uploads the specified file to G Drive."""
    store = file.Storage(path.join(JSON_LOCATION, 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path.join(JSON_LOCATION, 'credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    file_metadata = {
        'name': path.basename(file_path),
        'parents': [FOLDER_ID]
    }

    media = MediaFileUpload(file_path,
                            mimetype='image/png',
                            resumable=True)
    up_file = service.files().create(body=file_metadata,
                                     media_body=media,
                                     fields='id').execute()
    download_link = 'https://drive.google.com/uc?id={}&export=download'.format(up_file.get('id'))
    print(download_link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()
    upload_file(args.file_path)
