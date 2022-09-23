import os

GITHUB_JOB = "GITHUB_JOB"
FORCE_NO_VENV = "FORCE_NO_VENV"

# scripts ensures a virtual environment is located in .venv and is active

if __name__ == '__main__':

    is_inside_docker = os.path.exists('/.dockerenv')
    is_inside_gh_wf = GITHUB_JOB in os.environ
    is_force_no_venv = FORCE_NO_VENV in os.environ and os.environ[FORCE_NO_VENV] == "1"

    if is_inside_docker or is_inside_gh_wf or is_force_no_venv:
        exit(0)

    if not os.path.exists(f"{os.getcwd()}/.venv"):
        print(".venv directory not found")
        print("run cmd 'python -m venv .venv'")
        exit(1)

    if 'VIRTUAL_ENV' not in os.environ:
        print("virtual env is not active")
        print("run cmd '.venv\\Scripts\\activate'")
        exit(1)

    exit(0)
