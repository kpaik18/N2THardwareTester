from cmd.cli import app

import typer

if __name__ == "__main__":
    app()
    # fetcher: IHomeworkFetcher = ClassroomFetcher()
    # (
    #     homework_folder,
    #     student_submissions,
    #     course_id,
    #     coursework_id,
    #     course_students,
    # ) = fetcher.get_assignment_submissions("NTk1MzUxNTE3MjE4", "NTk3MDkxNTI5OTY3")
    # print(student_submissions)
    # print(course_id)
    # print(coursework_id)
    # print(course_students)
    # config_parser: IConfigurationParser = ConfigurationParser()
    # config = config_parser.parse_configuration_file("cmd/config_files/h2.yml")
    # tester: IHomeworkTester = HomeworkTester()
    # test_results = tester.test_homework_folder(homework_folder, config)
    # print(test_results)
    # grader: IGrader = ClassroomGrader()
    # grader.grade_homework(
    # "homework",
    #     course_students,
    #     student_submissions,
    #     test_results,
    #     "15jXXLvv4yTthiHvqEwJM3hcex--iEvOu",
    # )
