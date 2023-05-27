from configuration.configuration import ConfigurationParser, IConfigurationParser
from fetcher.fetcher import ClassroomFetcher, IHomeworkFetcher
from homeworktester.homework_tester import HomeworkTester, IHomeworkTester

if __name__ == "__main__":
    fetcher: IHomeworkFetcher = ClassroomFetcher()
    homework_folder = fetcher.get_assignment_submissions(
        "NTk1MzUxNTE3MjE4", "NTk1MzU1MjI4NzU0"
    )
    config_parser: IConfigurationParser = ConfigurationParser()
    config = config_parser.parse_configuration_file("h1.yml")
    tester: IHomeworkTester = HomeworkTester()
    print(tester.test_homework_folder(homework_folder, config))
