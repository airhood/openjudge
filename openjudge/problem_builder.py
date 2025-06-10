
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

        self.TC_count = 0
        self.checker = None
        self.time_limit = 2.0
        self.memory_limit = 256

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_input_description(self, input_description):
        self.input_description = input_description

    def set_output_description(self, output_description):
        self.output_description = output_description

    def set_constraints(self, constraints):
        self.constraints = constraints

    def set_examples(self, examples):
        self.examples = examples

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
