from dataclasses import dataclass


@dataclass
class TestResult:
    full_count: int
    passed_count: int
