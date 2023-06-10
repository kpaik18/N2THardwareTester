from configuration.configuration import ConfigurationParser, IConfigurationParser
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from grader.grader import ClassroomGrader, IGrader
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester

if __name__ == "__main__":
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    (
        homework_folder,
        student_submissions,
        course_id,
        coursework_id,
        course_students,
    ) = fetcher.get_assignment_submissions("NTk1MzUxNTE3MjE4", "NTk1MzU1MjI4NzU0")
    print(student_submissions)
    print(course_id)
    print(coursework_id)
    print(course_students)
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file("cmd/config_files/h1.yml")
    tester: IHomeworkTester = HomeworkTester()
    test_results = tester.test_homework_folder(homework_folder, config)
    print(test_results)
    grader: IGrader = ClassroomGrader()
    grader.grade_homework(
        course_students,
        student_submissions,
        test_results,
        "15jXXLvv4yTthiHvqEwJM3hcex--iEvOu",
    )
