# 📦 OpenJudge

**OpenJudge** is a lightweight Python package for running test cases on programs automatically. It’s designed to make local problem-solving and competitive programming development easier by simulating basic judge-like behavior.

## ✅ Features

- Run multiple test cases automatically
- Compare program output with expected output (with newline normalization)
- Highlight mismatches clearly
- Pretty test result summaries (e.g., `✔ [003]`)
- Cross-platform line-ending normalization (`\r\n` → `\n`)
- Configurable input/output folders

## 🚀 Installation

No installation required. Just download `autojudge.py` into your project.

## 📂 Folder Structure

problem/
├── your_program.py
├── tests/
│ ├── 001.in
│ ├── 001.out
│ ├── 002.in
│ └── 002.out

## ⚙️ Usage

In your test script:

```python
from openjudge import TC_Judge

tc_judge = TC_Judge()
tc_judge.load_TC(r'your testcase path', 50, 3)
tc_judge.load_code(r'your solution path')
tc_judge.set_time_limit(1000)
tc_judge.run()
tc_judge.print_results()
```