import os
import time
import subprocess
import psutil
import threading

def normalize_newlines(s):
    return s.replace('\r\n', '\n').strip()

class TC_Judge:
    def __init__(self):
        self.TC_in = []
        self.TC_out = []
        self.code_path = None
        self.time_limit = 2
        self.memory_limit = 256
        self.results = []

    def load_TC(self, tc_path, tc_count, format):
        if tc_path is None:
            raise ValueError("tc_path cannot be None")
        if tc_count is None:
            raise ValueError("tc_count cannot be None")
        if format is None:
            format = len(str(tc_count))
        if tc_count <= 0:
            raise ValueError("tc_count must be over 0")
        
        for i in range(1, tc_count + 1):
            fname = str(i).zfill(format)
            in_dir = os.path.join(tc_path, "test" + fname + ".in")
            out_dir = os.path.join(tc_path, "test" + fname + ".out")

            with open(in_dir, 'r') as file:
                input_read = file.read()
                print(f"[DEBUG] Loaded input TC{i}: {repr(input_read)}")
                self.TC_in.append(input_read)
            
            with open(out_dir, 'r') as file:
                output_read = file.read()
                print(f"[DEBUG] Loaded output TC{i}: {repr(output_read)}")
                self.TC_out.append(output_read)

    def load_code(self, code_path):
        print(f"[DEBUG] Loading code from: {code_path}")
        if code_path is None:
            raise ValueError("code_path cannot be None")
        self.code_path = code_path

    def set_time_limit(self, time_limit):
        print(f"[DEBUG] Setting time limit: {time_limit}")
        if time_limit is None:
            raise ValueError("time_limit cannot be None")
        if time_limit <= 0:
            raise ValueError("time_limit must be over 0")
        self.time_limit = time_limit

    def set_memory_limit(self, memory_limit):
        print(f"[DEBUG] Setting memory limit: {memory_limit}")
        if memory_limit is None:
            raise ValueError("memory_limit cannot be None")
        if memory_limit <= 0:
            raise ValueError("memory_limit must be over 0")
        self.memory_limit = memory_limit

    def run(self):
        print("[DEBUG] Running test cases...")
        self.results = []        
        for i in range(len(self.TC_in)):
            print(f"[DEBUG] Running TC #{i+1}")
            result = self.__run_cycle(self.TC_in[i], self.TC_out[i])
            self.results.append(result)

    def __run_cycle(self, input_data, output_data):
        try:
            print(f"\n[DEBUG] Running test case")
            print(f"[DEBUG] Input: {repr(input_data)}")
            print(f"[DEBUG] Expected Output: {repr(output_data)}")
            
            start_time = time.perf_counter()
            
            proc = subprocess.Popen(
                ["python", self.code_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            p = psutil.Process(proc.pid)
            mem_exceeded = False

            def monitor():
                nonlocal mem_exceeded
                while proc.poll() is None:
                    try:
                        mem = p.memory_info().rss / (1024 * 1024)  # MB
                        if self.memory_limit and mem > self.memory_limit:
                            mem_exceeded = True
                            proc.kill()
                            print(f"[DEBUG] Memory Limit Exceeded: {mem:.2f} MB")
                            break
                        time.sleep(0.01)
                    except psutil.NoSuchProcess:
                        break

            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()

            try:
                stdout, stderr = proc.communicate(input=input_data.encode('utf-8'), timeout=self.time_limit)
            except subprocess.TimeoutExpired:
                proc.kill()
                print(f"[DEBUG] Time Limit Exceeded")
                return {
                    "status": "TLE",
                    "message": "Time Limit Exceeded",
                    "elapsed_time": self.time_limit,
                    "return_code": -1
                }
            
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            test_output = stdout.decode("utf-8")
            print(f"[DEBUG] Actual Output: {repr(test_output)}")

            if mem_exceeded:
                return {
                    "status": "MLE",
                    "message": "Memory Limit Exceeded",
                    "elapsed_time": elapsed_time,
                    "return_code": -1
                }

            if proc.returncode != 0 or stderr:
                print(f"[DEBUG] Runtime Error: {stderr.decode('utf-8')}")
                return {
                    "status": "RE",
                    "message": f"Runtime Error: {stderr.decode('utf-8')}",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }

            if normalize_newlines(test_output.strip()) == normalize_newlines(output_data.strip()):
                print(f"[DEBUG] Verdict: AC")
                return {
                    "status": "AC",
                    "message": "Accepted",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }
            else:
                print(f"[DEBUG] Verdict: WA")
                return {
                    "status": "WA",
                    "message": "Wrong Answer",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }

        except Exception as e:
            print(f"[DEBUG] Unexpected Error: {type(e).__name__}: {e}")
            return {
                "status": "RE",
                "message": f"Runtime Error: {type(e).__name__}: {e}",
                "elapsed_time": 0,
                "return_code": None
            }

    def print_results(self):
        print("[DEBUG] Printing results...")
        for i in range(len(self.results)):
            status = self.results[i]["status"]
            elapsed_time = self.results[i]["elapsed_time"] * 1000 # ms
            if status == "AC":
                print(f"[TC {i+1}] ✅ AC (elapsed_time: {elapsed_time:.2f}ms)")
            elif status == "WA":
                print(f"[TC {i+1}] ❌ WA (elapsed_time: {elapsed_time:.2f}ms)")
            elif status == "RE":
                print(f"[TC {i+1}] 🛑 RE")
            elif status == "TLE":
                print(f"[TC {i+1}] ⌛ TLE (elapsed_time: {elapsed_time:.2f}ms)")

    def clear_results(self):
        print("[DEBUG] Clearing results...")
        self.results = []

    def reset(self):
        print("[DEBUG] Resetting judge...")
        self.TC_in = []
        self.TC_out = []
        self.code_path = None
        self.time_limit = None
        self.results = []


class Checker_Judge:
    def __init__(self):
        self.TC_in = []
        self.checker_path = None
        self.code_path = None
        self.time_limit = None
        self.results = []

    def load_TC(self, tc_path, tc_count, format):
        print(f"[DEBUG] Loading {tc_count} test cases from: {tc_path}")
        if tc_path is None:
            raise ValueError("tc_path cannot be None")
        if tc_count is None:
            raise ValueError("tc_count cannot be None")
        if format is None:
            format = len(str(tc_count))
        if tc_count <= 0:
            raise ValueError("tc_count must be over 0")
        
        for i in range(1, tc_count + 1):
            fname = str(i).zfill(format)
            in_dir = os.path.join(tc_path, fname + ".in")

            with open(in_dir, 'r') as file:
                input_read = file.read()
                self.TC_in.append(input_read)
        print("[DEBUG] Finished loading test cases.")

    def load_checker(self, checker_path):
        print(f"[DEBUG] Loading checker from: {checker_path}")
        if checker_path is None:
            raise ValueError("checker_path cannot be None")
        self.checker_path = checker_path

    def load_code(self, code_path):
        print(f"[DEBUG] Loading code from: {code_path}")
        if code_path is None:
            raise ValueError("code_path cannot be None")
        self.code_path = code_path

    def set_time_limit(self, time_limit):
        print(f"[DEBUG] Setting time limit: {time_limit}")
        if time_limit is None:
            raise ValueError("time_limit cannot be None")
        if time_limit <= 0:
            raise ValueError("time_limit must be over 0")
        self.time_limit = time_limit

    def set_memory_limit(self, memory_limit):
        print(f"[DEBUG] Setting memory limit: {memory_limit}")
        if memory_limit is None:
            raise ValueError("memory_limit cannot be None")
        if memory_limit <= 0:
            raise ValueError("memory_limit must be over 0")
        self.memory_limit = memory_limit

    def run(self):
        print("[DEBUG] Running test cases with checker...")
        self.results = []
        time_limit = self.time_limit or 2.0

        for i in range(len(self.TC_in)):
            print(f"[DEBUG] Running TC #{i+1}")
            result = self.run_cycle(self.TC_in[i], time_limit=time_limit)
            self.results.append(result)

    def run_cycle(self, input_data, time_limit=2.0):
        try:
            start_time = time.perf_counter()

            proc = subprocess.Popen(
                ["python", self.code_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            p = psutil.Process(proc.pid)
            mem_exceeded = False

            def monitor():
                nonlocal mem_exceeded
                while proc.poll() is None:
                    mem = p.memory_info().rss / (1024 * 1024)
                    if self.memory_limit and mem > self.memory_limit:
                        mem_exceeded = True
                        proc.kill()
                        break
                    time.sleep(0.01)
                
            monitor_thread = threading.Thread(target=monitor)
            monitor_thread.start()

            try:
                stdout, stderr = proc.communicate(input=input_data.encode('utf-8'), timeout=self.time_limit)
            except subprocess.TimeoutExpired:
                proc.kill()
                return {
                    "status": "TLE",
                    "message": "Time Limit Exceeded",
                    "elapsed_time": self.time_limit,
                    "return_code": -1
                }

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            if mem_exceeded:
                return {
                    "status": "MLE",
                    "message": "Memory Limit Exceeded",
                    "elapsed_time": elapsed_time,
                    "return_code": -1
                }

            if proc.returncode != 0 or stderr:
                return {
                    "status": "RE",
                    "message": f"Runtime Error: {stderr.decode('utf-8')}",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }

            test_output = stdout.decode("utf-8")

            checker_result = subprocess.run(
                ["python", self.checker_path],
                input = input_data.encode("utf-8"),
                capture_output=True,
                timeout=1.0
            )

            output_data = checker_result.stdout.decode("utf-8")

            if normalize_newlines(test_output.strip()) == normalize_newlines(output_data.strip()):
                return {
                    "status": "AC",
                    "message": "Accepted",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }
            else:
                return {
                    "status": "WA",
                    "message": "Wrong Answer",
                    "elapsed_time": elapsed_time,
                    "return_code": proc.returncode
                }

        except Exception as e:
            return {
                "status": "RE",
                "message": f"Runtime Error: {type(e).__name__}: {e}",
                "elapsed_time": 0,
                "return_code": None
            }

    def print_results(self):
        print("[DEBUG] Printing results...")
        for i in range(len(self.results)):
            status = self.results[i]["status"]
            elapsed_time = self.results[i]["elapsed_time"] * 1000
            if status == "AC":
                print(f"[TC {i+1}] ✅ AC (elapsed_time: {elapsed_time:.2f}ms)")
            elif status == "WA":
                print(f"[TC {i+1}] ❌ WA (elapsed_time: {elapsed_time:.2f}ms)")
            elif status == "RE":
                print(f"[TC {i+1}] 🛑 RE")
            elif status == "TLE":
                print(f"[TC {i+1}] ⌛ TLE (elapsed_time: {elapsed_time:.2f}ms)")

    def clear_results(self):
        print("[DEBUG] Clearing results...")
        self.results = []

    def reset(self):
        print("[DEBUG] Resetting judge...")
        self.TC_in = []
        self.checker_path = None
        self.code_path = None
        self.time_limit = None
        self.results = []
