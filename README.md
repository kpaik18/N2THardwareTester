# N2T Hardware Tester
Command Line Application to test nand2tetris hardware homeworks.

## Description
The N2T Hardware Tester is a command-line tool designed to help course facilitators test the first five assignments of the nand2tetris hardware course. It provides functionality to check and grade student assignments.

## Installation
To use the N2T Hardware Tester, install it using the following command:

pip install n2t-hardware-tester

# Commands for Students
## Testing Archived Homeworks
To check their archived homework, students can use the following command:

n2t-test test-homework [command] [homework] [zip_file_address]

homework should be one of the following values: h1, h2, h3, h4, h5.

zip_file_address should be the path to the zipped homework file on the student's machine.

## Environment Variables for Students
n2t_work_area_path: Path of the nand2tetris folder that contains tools and project directories.

# Commands for Lecturers or Assistants
## Grading Student Assignments
To grade student assignments, lecturers or assistants can use the following command:

n2t-test grade-homework [command] [homework] [course_code] [coursework_code] [drive_folder_id] [late_days_percentages]

homework should be one of the following values: h1, h2, h3, h4, h5.

course_code can be found in the URL of the classroom.

coursework_code can be found in the URL of the classroom assignment.

drive_folder_id can be found in the URL of the Google Drive folder.

late_days_percentages should be provided as a series of pairs: [late_day_count] [percentage_loss], separated by spaces. For example, "1 20 2 50" means that for one late day, the student loses 20%, and for two late days, the student loses 50%. If late days are not allowed, use "1 100" as the argument.

## Environment Variables for Lecturers or Assistants

n2t_work_area_path: Path of the nand2tetris folder that contains tools and project directories.

n2t_google_api_credentials: API credentials path for the Google Cloud Console project.

n2t_google_api_tokens_path: Path for the API tokens, which will be generated automatically after login.

n2t_homework_files_download_folder: Path of the folder where student assignments will be downloaded.

# License

MIT License

# Contact

For any inquiries or support, please contact Koba Paikidze(kpaik18@freeuni.edu.ge).

Feel free to modify and expand upon this template to include any additional information or sections that are relevant to your project.
