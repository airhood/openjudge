import os

class TC_Generator:
    def __init__(self):
        self.TC_path = None
        self.TC_checker_path = None
        
    def set_TC_path(self, TC_path):
        if TC_path is None:
            raise ValueError("TC_path cannot be None")
        self.TC_path = TC_path

    def set_TC_checker(self, TC_checker_path):
        self.TC_checker_path = TC_checker_path

    def generate(self, TC_count, format):
        if TC_count is None:
            raise ValueError("TC_count cannot be None")
        if TC_count <= 0:
            raise ValueError("TC_count must be over zero")
        
        if self.TC_path == None:
            raise ValueError("TC_path should be set before generating testcases")
        
        for i in range(1, TC_count + 1):
            fname = str(i).zfill(format)
            in_path = os.path.join(self.TC_path, "test" + fname + ".in")
            out_path = os.path.join(self.TC_path, "test" + fname + ".out")

            with open(in_path, "w") as file:
                pass

            with open(out_path, "w") as file:
                pass
