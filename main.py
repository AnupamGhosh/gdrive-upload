import argparse
import logging
import sys

from drive_upload import GoogleDriveUpload
from listener import Listener

def main(arglist):
  logging.basicConfig(format='%(funcName)s:%(lineno)d %(levelname)s %(message)s', level=logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '-mode', dest='mode', default=RUN_MODE.UPLOAD, help='The mdoe to run Good drive uploader',
    choices=RUN_MODE.CHOICES
  )
  parser.add_argument(
    '--upload', dest='upload', default='', help='Upload a file or directory'
  )
  args = parser.parse_args(arglist[1:])

  if args.mode == RUN_MODE.UPLOAD:
    if not args.upload:
      raise ValueError('params --upload required')
    GoogleDriveUpload.upload_in_shared(args.upload)

  elif args.mode == RUN_MODE.LISTENER:
    PORT = 4242
    IP = '127.0.0.1'
    uploader = GoogleDriveUpload()
    listener = Listener(IP, PORT, uploader)
    listener.listen()

class RUN_MODE():
  UPLOAD = 0
  LISTENER = 1
  CHOICES = (UPLOAD, LISTENER)

if __name__ == "__main__":
    main(sys.argv)