from typing import Protocol

from googleapiclient.discovery import build

from authutil.auth_util import auth_on_google_classroom


class IGrader(Protocol):
    def grade_homework(self, student_submissions, test_results):
        pass


class ClassroomGrader:
    def grade_homework(self, student_submissions, test_results, drive_folder_id):
        self._create_google_sheet(drive_folder_id)

    def _create_google_sheet(self, drive_folder_id):
        creds = auth_on_google_classroom()
        service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": "My Spreadsheet",
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "parents": [drive_folder_id],
        }
        file = service.files().create(body=file_metadata).execute()

        file_id = file["id"]
        print(file)
