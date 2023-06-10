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
    ) = fetcher.get_assignment_submissions("NjEyMDE2MDkyOTky", "NjEyOTA1NjY1MjM0")
    print(student_submissions)
    print(course_id)
    print(coursework_id)
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file("h1.yml")
    tester: IHomeworkTester = HomeworkTester()
    test_results = tester.test_homework_folder(homework_folder, config)
    print(test_results)
    grader: IGrader = ClassroomGrader()
    grader.grade_homework(
        course_id,
        coursework_id,
        student_submissions[0].student_id,
        student_submissions[0].submission_id,
        test_results[0],
    )
