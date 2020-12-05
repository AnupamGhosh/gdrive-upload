import os
import logging

from pathlib import Path
from googleapiclient.http import MediaFileUpload

from drive_service import GoogleDriveService
from scan_dir import DirectoryScanner

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
    return folder['id']

  def upload_file(self, path: str, drive_dir_id: str): # '1YnTQoIuk8J6780G-kLKdNZkuVZAAin04'
    filename = os.path.basename(path)
    file_metadata = {'name': filename, 'parents': [drive_dir_id]}
    media = MediaFileUpload(path, resumable=True)
    res = self.create_drive_file({
      'body': file_metadata,
      'media_body': media,
      'fields': 'id'
    })
    logging.info('%s uploaded. FIle ID: %s', path, res.get('id'))
    return res

  def upload(self, upload_file: str, drive_dir_id: str):
    '''the path which will get uploaded to google drive'''
    dir_uploader = GdriveUploadDirectory(self)
    dir_uploader.upload(upload_file, drive_dir_id)


  def create_drive_file(self, create_params):
    res = self.drive.files().create(**create_params).execute() # pylint: disable=no-member
    return res

  def handle_request(self, message):
    path = message.get('path')
    drive_dir_id = message.get('drive_dir')
    self.upload(path, drive_dir_id)

  # temp function
  @staticmethod
  def upload_in_shared(path: str):
    logging.info('Starting Upload')
    GoogleDriveUpload().upload(path, '1P2KC1nZFjjySzJKQH6MoGVL_QXV4C3-e')
    logging.info('Upload Done!')

class GdriveUploadDirectory(DirectoryScanner):
  def __init__(self, uploader):
    self.uploader = uploader
    self.dir_ids = {} # maps local directory with drive directory

  def file_found(self, path):
    upload_to = self.get_drive_id(path.parent)
    res = self.uploader.upload_file(str(path), upload_to)
    return res

  def dir_found(self, path):
    upload_to = self.get_drive_id(path.parent) # upload directory in parent's drive id
    drive_id = self.uploader.create_dir(path.name, upload_to) # returns location id of path
    self.dir_ids[self.path_id(path)] = drive_id
    return drive_id

  def path_id(self, path: Path):
    return path.stat().st_ino

  def get_drive_id(self, path: Path):
    parent_id = self.path_id(path)
    upload_to = self.dir_ids[parent_id]
    return upload_to

  def upload(self, upload_dir: str, upload_to: str):
    parent_path = Path(upload_dir).parent
    self.dir_ids[self.path_id(parent_path)] = upload_to
    super().scan(upload_dir)

def main():
  secret_path = os.path.join(os.path.dirname(__file__), 'secrets')
  uploader = GoogleDriveUpload()
  uploader.upload(secret_path, '1OM5tcSl0QnzDjNO6LMrVpgb8faS586pz')

if __name__ == "__main__":
  main()
