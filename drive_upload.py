import os
import logging

from googleapiclient.http import MediaFileUpload

from drive_service import GoogleDriveService

class GoogleDriveUpload():
  def __init__(self, drive_service: GoogleDriveService):
    self.drive = drive_service.get()

  def upload(self, path: str, drive_dir_id: str): # '1YnTQoIuk8J6780G-kLKdNZkuVZAAin04'
    filename = os.path.basename(path)
    file_metadata = {'name': filename, 'parents': [drive_dir_id]}
    media = MediaFileUpload(path, resumable=True)
    res = self.drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
    logging.info('%s uploaded. FIle ID: %s', path, res.get('id'))


path = os.path.join(os.path.dirname(__file__), 'file.txt')
drive_service = GoogleDriveService()
uploader = GoogleDriveUpload(drive_service)
uploader.upload(path, '1job7FAIJqmDYlqStVqodk4q_DfEYZKBo')