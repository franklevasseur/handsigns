import argparse
import os
from functools import cmp_to_key

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

# scripts sorts requirements.txt if needed


def default_compare(dep_a: str, dep_b: str):
    if dep_a < dep_b:
        return -1
    if dep_a > dep_b:
        return +1
    return 0


def custom_compare(dep_a: str, dep_b: str):

    dep_a = dep_a.lower().split("==")[0]
    dep_b = dep_b.lower().split("==")[0]

    len_a = len(dep_a)
    len_b = len(dep_b)

    if len_a < len_b and dep_b.startswith(dep_a):
        return -1

    if len_b < len_a and dep_a.startswith(dep_b):
        return +1

    return default_compare(dep_a, dep_b)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run E2e Tests on OpenBook Server.")
    parser.add_argument("--requirements", "-r", type=str, required=True, help="location of requirements file to sort.")
    parser.add_argument("--check-only", "-c", action=argparse.BooleanOptionalAction,
                        required=False, help="location of requirements file to sort.")
    args = parser.parse_args()

    requirements_path = args.requirements
    check_only = args.check_only

    with open(requirements_path, 'r') as fd:
        file_content = fd.read().strip()

    dependencies = file_content.splitlines()
    sorted_dependencies = list(set(dependencies))
    sorted_dependencies.sort(key=cmp_to_key(custom_compare))

    sorted_content = '\n'.join(sorted_dependencies).strip()

    if check_only:
        if sorted_content != file_content:
            print(file_content)
            print(f'"{os.path.basename(requirements_path)}" not sorted. run cmd "make format".')
            exit(1)
        print(f'"{os.path.basename(requirements_path)}" is already sorted.')
        exit(0)

    with open(requirements_path, 'w') as fd:
        fd.write(f"{sorted_content}\n")

    exit(0)
