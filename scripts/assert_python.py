from platform import python_version

current_py_version = python_version()
target_py_version = open(".python-version", "r").read().strip()

if current_py_version != target_py_version:
    print(f"Expected Python version '{target_py_version}' but found '{current_py_version}'")
    exit(1)

exit(0)
