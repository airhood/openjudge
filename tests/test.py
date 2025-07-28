import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from openjudge import TC_Judge, Checker_Judge

tc_judge = TC_Judge()
tc_judge.load_TC(r'C:\Users\airhood\Documents\git\openjudge\data\problem 1\testcase', 10, 3)
tc_judge.load_code(r'C:\Users\airhood\Documents\git\openjudge\data\problem 1\solution.py')
tc_judge.set_time_limit(1000)
tc_judge.run()
tc_judge.print_results()

print("\n\n========================================\n\n")

checker_judge = Checker_Judge()
checker_judge.load_checker(r'C:\Users\airhood\Documents\git\openjudge\data\problem 2\checker.py')
checker_judge.load_TC(r'C:\Users\airhood\Documents\git\openjudge\data\problem 2\testcase', 2, 3)
checker_judge.load_code(r'C:\Users\airhood\Documents\git\openjudge\data\problem 2\solution.py')
checker_judge.set_time_limit(1000)
checker_judge.run()
checker_judge.print_results()