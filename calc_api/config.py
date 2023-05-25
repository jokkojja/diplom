from googleapiclient.discovery import build
from google.oauth2 import service_account

CALCULATOR_PATH = "calculating_waves"
PROG_NAME_CPP = 'progr.cpp'
PROG_NAME_EXE = 'progr'

#google drive
scope = ['https://www.googleapis.com/auth/drive']
key_file_location = '/Users/jokkojja/Desktop/diplom/diplom/google_drive/hopeful-sound-387705-801fd71458ae.json'
credentials = service_account.Credentials.from_service_account_file(
key_file_location)

scoped_credentials = credentials.with_scopes(scope)
service = build('drive', 'v3', credentials=scoped_credentials)