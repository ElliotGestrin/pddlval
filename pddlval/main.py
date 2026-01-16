import subprocess
import tempfile
import platform
import sys
import os

def validate_domain(domain: str) -> bool:
    """
    Use VAL to validate the given PDDL domain file or content.

    Args:
        domain (str): Path to the PDDL domain file, or the content of the domain.
    """
    domain_file, is_temp_domain = prepare_file_or_content(domain)
    parser_executable = get_parser_executable()
    try:
        result = subprocess.run([parser_executable, domain_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        # Parser returns 0 even with errors, so we need to check the output
        if "Errors: 0, warnings: 0" in result.stdout:
            return True
        else:
            return False
    finally:
        if is_temp_domain:
            os.remove(domain_file)

def validate_problem(domain: str, problem: str) -> bool:
    """
    Use VAL to validate if the given problem is well-formed with respect to the specified domain.

    Args:
        domain (str): Path to the PDDL domain file, or the content of the domain.
        problem (str): Path to the PDDL problem file, or the content of the problem.
    """
    domain_file, is_temp_domain = prepare_file_or_content(domain)
    problem_file, is_temp_problem = prepare_file_or_content(problem)
    parser_executable = get_parser_executable()
    try:
        result = subprocess.run([parser_executable, domain_file, problem_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        # Parser returns 0 even with errors, so we need to check the output
        if "Errors: 0, warnings: 0" in result.stdout:
            return True
        else:
            return False
    finally:
        if is_temp_domain:
            os.remove(domain_file)
        if is_temp_problem:
            os.remove(problem_file)

def validate_plan(domain: str, problem: str, plan: str) -> bool:
    """
    Use VAL to validate if the given plan solves the problem in the specified domain.

    Args:
        domain (str): Path to the PDDL domain file, or the content of the domain.
        problem (str): Path to the PDDL problem file, or the content of the problem.
        plan (str): Path to the plan file, or the content of the plan.
    """
    domain_file, is_temp_domain = prepare_file_or_content(domain)
    problem_file, is_temp_problem = prepare_file_or_content(problem)
    plan_file, is_temp_plan = prepare_file_or_content(plan)
    val_executable = get_val_executable()
    try:
        result = subprocess.run([val_executable, domain_file, problem_file, plan_file],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        # Check the output for success/failure indicators
        output = result.stdout + result.stderr
        
        # VAL returns 0 even with errors, so we need to check the output
        # Look for success indicator
        if "Plan valid" in output:
            return True
        # Look for error indicators
        elif any(indicator in output for indicator in ["Error:", "Bad plan description!", "Failed plans:", "Bad operator in plan!"]):
            return False
        # If return code is non-zero, it's definitely a failure
        elif result.returncode != 0:
            return False
        else:
            # Default to False if we can't determine validity
            return False
    finally:
        if is_temp_domain:
            os.remove(domain_file)
        if is_temp_problem:
            os.remove(problem_file)
        if is_temp_plan:
            os.remove(plan_file)

def validate(domain: str, problem: str | None = None, plan: str | None = None) -> bool:
    """
    General validation function that determines what to validate based on provided arguments.

    Args:
        domain (str): Path to the PDDL domain file, or the content of the domain.
        problem (str | None): Path to the PDDL problem file, or the content of the problem.
        plan (str | None): Path to the plan file, or the content of the plan.
    """
    if plan:
        assert domain is not None, "Domain must be provided when validating a plan."
        assert problem is not None, "Problem must be provided when validating a plan."
        return validate_plan(domain, problem, plan)
    elif problem:
        assert domain is not None, "Domain must be provided when validating a problem."
        return validate_problem(domain, problem)
    elif domain:
        return validate_domain(domain)
    else:
        raise ValueError("At least one of domain, problem, or plan must be provided for validation.")
    
def prepare_file_or_content(arg: str) -> tuple[str, bool]:
    """
    Prepare the argument for VAL. If it's a file path, return it as is.
    If it's content, write it to a temporary file and return the file path.

    Args:
        arg (str): The file path or content.

    Returns:
        tuple[str, bool]: The file path to be used with VAL and a boolean indicating if it's a temporary file.
    """

    if os.path.isfile(arg):
        return arg, False
    else:
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.pddl')
        temp_file.write(arg)
        temp_file.close()
        return temp_file.name, True
    
def get_executable_dir() -> str:
    file_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(file_path)
    os_name = sys.platform
    if os_name.startswith("win"):
        if platform.architecture()[0] != "64bit":
            raise RuntimeError("Only 64-bit Windows is supported")
        subdir = "windows"
    elif os_name.startswith("linux"):
        subdir = "linux"
    elif os_name.startswith("darwin"):
        subdir = "macos"
    else:
        raise RuntimeError(f"Unsupported OS: {os_name}")
    return os.path.join(dir_path, "binaries", subdir)
    
def get_val_executable() -> str:
    """
    Get the Validate executable path.

    Returns:
        str: The path to the Validate executable.
    """
    exe_name = "Validate.exe" if sys.platform.startswith("win") else "Validate"
    return os.path.join(get_executable_dir(), exe_name)

def get_parser_executable() -> str:
    """
    Get the Parser executable path.

    Returns:
        str: The path to the Parser executable.
    """
    exe_name = "Parser.exe" if sys.platform.startswith("win") else "Parser"
    return os.path.join(get_executable_dir(), exe_name)