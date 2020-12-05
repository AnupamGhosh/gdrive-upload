import os
import logging

from googleapiclient.http import MediaFileUpload

from drive_service import GoogleDriveService

class GoogleDriveUpload():
  def __init__(self):
    drive_service = GoogleDriveService()
    self.drive = drive_service.get()

  def create_dir(self, dir_name, parent_dir_id):
    file_metadata = {
        'name': dir_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_dir_id]
    }
    folder = self.create_drive_file({
      'body': file_metadata,
      'fields': 'id'
    })
    print(f'folder={folder}')
    return folder['id']

  def upload(self, path: str, drive_dir_id: str): # '1YnTQoIuk8J6780G-kLKdNZkuVZAAin04'
    filename = os.path.basename(path)
    file_metadata = {'name': filename, 'parents': [drive_dir_id]}
    media = MediaFileUpload(path, resumable=True)
    res = self.create_drive_file({
      'body': file_metadata,
      'media_body': media,
      'fields': 'id'
    })
    print(f'file_id={res}')
    logging.info('%s uploaded. FIle ID: %s', path, res.get('id'))

  def create_drive_file(self, create_params):
    res = self.drive.files().create(**create_params).execute() # pylint: disable=no-member
    return res

  def handle_request(self, message):
    path = message.get('path')
    drive_dir_id = message.get('drive_dir')
    self.upload(path, drive_dir_id)

def main():
  path = os.path.join(os.path.dirname(__file__), 'file.txt')
  uploader = GoogleDriveUpload()
  dir_id = uploader.create_dir('secrets', '1lvZ8eGPS-pFd8APBnIcVikAh6sr3diVs')
  uploader.upload(path, dir_id)

if __name__ == "__main__":
  main()
