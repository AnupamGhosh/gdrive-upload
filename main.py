import logging

from drive_upload import GoogleDriveUpload
from listener import Listener

def main():
  logging.basicConfig(format='%(funcName)s:%(lineno)d %(levelname)s %(message)s', level=logging.INFO)
  PORT = 4242
  IP = '127.0.0.1'
  uploader = GoogleDriveUpload()
  listener = Listener(IP, PORT, uploader)
  listener.listen()

if __name__ == "__main__":
    main()