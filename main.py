import os

from configuration.configuration import Configuration
from homeworktester.single_tester import (
    ISingleHomeworkTester,
    SingleHomeworkTester,
)

if __name__ == "__main__":
    single_tester: ISingleHomeworkTester = SingleHomeworkTester()
    res = single_tester.test_homework(
        os.path.join("C:/Users/Surface/Desktop/nglun20.zip"),
        Configuration(
            "zip",
            [
                "Not.hdl",
                "And.hdl",
                "Or.hdl",
                "Xor.hdl",
                "Mux.hdl",
                "DMux.hdl",
                "And16.hdl",
            ],
            ["Not.tst", "And.tst", "Or.tst", "Xor.tst", "Mux.tst", "DMux.tst"],
        ),
        "01",
    )
    print(res)
