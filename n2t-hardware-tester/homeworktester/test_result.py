from dataclasses import dataclass


@dataclass
class TestResult:
    name: str
    full_count: int
    passed_count: int
