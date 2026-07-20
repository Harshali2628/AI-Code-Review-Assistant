from utils.pytest_runner import run_pytest

success, output = run_pytest("test_generated.py")

print(success)
print(output)