from configuration.configuration import ConfigurationParser, IConfigurationParser
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester

if __name__ == "__main__":
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    (
        homework_folder,
        student_submissions,
        course_id,
        coursework_id,
        course_students,
    ) = fetcher.get_assignment_submissions("NjEyMDE2MDkyOTky", "NjEyMDE1OTg3ODg3")
    print(student_submissions)
    print(course_id)
    print(coursework_id)
    print(course_students)
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file("h1.yml")
    tester: IHomeworkTester = HomeworkTester()
    test_results = tester.test_homework_folder(homework_folder, config)
    print(test_results)
