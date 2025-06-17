from openjudge import TC_Judge

tc_judge = TC_Judge()
tc_judge.load_TC(r'C:\Users\airhood\Documents\git\openjudge\data\problem 1\testcase', 50, 3)
tc_judge.load_code(r'C:\Users\airhood\Documents\git\openjudge\data\problem 1\solution.py')
tc_judge.set_time_limit(1000)
tc_judge.run()
tc_judge.print_results()