from typing import List
from enum import Enum

class JudgeType(Enum):
    TEST_CASE = 0
    CHECKER = 1

class ProblemBuilder:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.input_description = ""
        self.output_description = ""
        self.constraints = ""
        self.examples = ""

        self.difficulty = ""
        self.tags = []
        self.author = ""

        self.judge_type = JudgeType.TEST_CASE
        self.TC_count = 0
        self.TC_path = None
        self.checker_path = None
        self.time_limit = 2.0
        self.memory_limit = 256

    def set_title(self, title: str):
        self.title = title
        return self

    def set_description(self, description: str):
        self.description = description
        return self

    def set_input_description(self, input_description: str):
        self.input_description = input_description
        return self

    def set_output_description(self, output_description: str):
        self.output_description = output_description
        return self

    def set_constraints(self, constraints: str):
        self.constraints = constraints
        return self

    def set_examples(self, examples: str):
        self.examples = examples
        return self

    def set_difficulty(self, difficulty: str):
        self.difficulty = difficulty
        return self

    def set_tags(self, tags: List[str]):
        self.tags = tags
        return self

    def add_tag(self, tag: str):
        self.tags.append(tag)
        return self

    def set_author(self, author: str):
        self.author = author
        return self

    def set_judge_type(self, judge_type: JudgeType):
        self.judge_type = judge_type
        return self

    def set_TC_count(self, TC_count: int):
        if self.judge_type != JudgeType.TEST_CASE:
            raise Exception("set_TC_count can only be used when judge type is TEST_CASE")
        self.TC_count = TC_count
        return self

    def set_TC_path(self, TC_path: str):
        if self.judge_type != JudgeType.TEST_CASE:
            raise Exception("set_TC_count can only be used when judge type is TEST_CASE")
        self.TC_path = TC_path
        return self

    def set_checker_path(self, checker_path: str):
        if self.judge_type != JudgeType.CHECKER:
            raise Exception("set_TC_count can only be used when judge type is CHECKER")
        self.checker_path = checker_path
        return self

    def set_time_limit(self, time_limit: int):
        self.time_limit = time_limit
        return self

    def set_memory_limit(self, memory_limit: int):
        self.memory_limit = memory_limit
        return self
    
    def build(self):
        pass