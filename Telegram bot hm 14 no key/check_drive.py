from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

from config.config import Config


SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(Config.GOOGLE_KEY_PATH, scopes=SCOPES)
drive = build("drive", "v3", credentials=creds)

content = b"drive ping"
media = MediaInMemoryUpload(content, mimetype="text/plain")

file_metadata = {
    "name": "drive_test.txt",
    "parents": [Config.DRIVE_FOLDER_ID],
}

created = drive.files().create(
    body=file_metadata,
    media_body=media,
    fields="id,name,webViewLink,parents",
).execute()

print("UPLOADED:", created["name"])
print("ID:", created["id"])
print("LINK:", created.get("webViewLink"))
