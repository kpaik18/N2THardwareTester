import os

from configuration.configuration import Configuration, ConfigurationParser
from homeworktester.homework_tester import (
    IHomeworkTester,
    HomeworkTester,
)

if __name__ == "__main__":
    tester: IHomeworkTester = HomeworkTester()
    tester.test_homework_folder('C:/Users/Surface/Desktop/homeworks',
                                ConfigurationParser().parse_configuration_file('hw1.yml')
                                )
    # res = single_tester.test_homework(
    #     os.path.join("C:/Users/Surface/Desktop/nglun20.zip"),
    #     Configuration(
    #         "zip",
    #         [
    #             "Not.hdl",
    #             "And.hdl",
    #             "Or.hdl",
    #             "Xor.hdl",
    #             "Mux.hdl",
    #             "DMux.hdl",
    #             "And16.hdl",
    #         ],
    #         ["Not.tst", "And.tst", "Or.tst", "Xor.tst", "Mux.tst", "DMux.tst"],
    #     ),
    #     "01",
    # )
    # print(res)
