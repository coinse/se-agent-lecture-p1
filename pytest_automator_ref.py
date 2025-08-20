import logging

import os
import time
import shutil
import glob
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pytest-automator")

PYTHON_PATH = "/Users/greenmon/Dropbox/Projects/agent-building-lecture-2025summer/venv/bin/python"

os.environ["COVERAGE_FILE"] = os.path.join(os.path.dirname(__file__), ".coverage")

@mcp.tool()
def list_files() -> str:
    """
    List all Python files in the target directory to generate tests for.
    """
    target_dir = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs")

    file_list = []
    for file_path in glob.glob(os.path.join(target_dir, "*/*.py")):
        file_list.append(file_path.removeprefix(target_dir + os.sep))

    try:
        files = "\n".join(file_list)
        return f"All Python files in the target directory:\n{files}"
    except Exception as e:
        return f"Error listing files: {str(e)}"

@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Read the contents of a Python file in the target directory to generate tests for.
    Args:
        file_path (str): The path of the Python file to read.
    """
    if not file_path.endswith('.py'):
        file_path += '.py'  # 처음부터 넣도록 유도하는 게 아니라 한번 Claude랑 연결해 보고, Claude가 파일 이름에 .py를 제외하고 실행하는 것을 확인한 후 처리해주도록 유도

    full_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", file_path)
    try:
        with open(full_file_path, 'r') as file:
            content = file.read()
        return f"{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@mcp.tool()
def read_file_with_line_numbers(file_path: str) -> str:
    """
    Read the contents of a Python file in the target directory to generate tests for with line numbers annotated.
    Args:
        file_path (str): The path of the Python file to read.
    """
    if not file_path.endswith('.py'):
        file_path += '.py'  # 처음부터 넣도록 유도하는 게 아니라 한번 Claude랑 연결해 보고, Claude가 파일 이름에 .py를 제외하고 실행하는 것을 확인한 후 처리해주도록 유도

    full_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", file_path)
    try:
        with open(full_file_path, 'r') as file:
            content_lines = file.readlines()
        content = "\n".join(f"{i + 1}: {line.strip()}" for i, line in enumerate(content_lines))
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a Python file in the target directory.
    Args:
        file_path (str): The path of the file to write.
        content (str): The content to write to the file.
    """
    if not file_path.endswith('.py'):
        file_path += '.py'

    full_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", file_path)
    try:
        with open(full_file_path, 'w') as file:
            file.write(content)
        return f"Successfully wrote to {file_path}."
    except Exception as e:
        return f"Error writing file: {str(e)}"


@mcp.tool()
def run_pytest(test_file_path: str) -> str:
    """
    Run pytest on the given Python test file in the target directory.
    Args:
        test_file_path (str): The path of the Python test file to run.
    """
    if not test_file_path.endswith('.py'):
        test_file_path += '.py'

    test_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", test_file_path)
    try:
        result = subprocess.run([PYTHON_PATH, "-m", 'pytest', test_file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return f"Tests passed successfully. Output:\n{result.stdout}"
        else:
            return f"Tests failed. Output:\n{result.stdout}{result.stderr}"
    except Exception as e:
        return f"Error running pytest: {str(e)}"


@mcp.tool()
def measure_coverage(test_file_path: str) -> str:
    """
    Measure code coverage for the generated test files in the target directory.
    Args:
        test_file_path (str): The path of the Python test file to run.
    """
    if not test_file_path.endswith('.py'):
        test_file_path += '.py'

    test_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", test_file_path)
    try:
        result = subprocess.run([PYTHON_PATH, "-m", 'coverage', 'run', '-m', 'pytest', test_file_path], capture_output=True, text=True)
        if result.returncode == 0:
            coverage_result = subprocess.run([PYTHON_PATH, "-m", 'coverage', 'report', '-m'], capture_output=True, text=True)
            return f"Coverage report:\n{coverage_result.stdout}"
        else:
            return f"Error running coverage: {result.stdout}{result.stderr}"
    except Exception as e:
        return f"Error measuring coverage: {str(e)}"


@mcp.tool()
def run_pynguin(file_path: str) -> str:
    """
    Run Pynguin (Search-based Automated Unit Test Generation for Python) on the given Python file to automatically generate tests.
    Args:
        file_path (str): The path of the Python file to run Pynguin on.
    """
    if not file_path.endswith('.py'):
        file_path += '.py'

    full_file_path = os.path.join(os.path.dirname(__file__), "target_programs", "human-eval", "dirs", file_path)
    project_path = os.path.dirname(full_file_path)
    module_name = os.path.basename(full_file_path).removesuffix('.py')

    local_env = os.environ.copy()
    local_env["PYNGUIN_DANGER_AWARE"] = "1"

    try:
        temp_output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp_pynguin_output'))
        os.makedirs(temp_output_path, exist_ok=True)
        result = subprocess.run([PYTHON_PATH, "-m", 'pynguin', '--project-path', project_path, '--module-name', module_name, '--output-path', temp_output_path, '--report-dir', temp_output_path, '--maximum_search_time', '30'], capture_output=True, text=True, env=local_env)
        if result.returncode == 0:
            # Copy the generated test file to the target directory
            generated_test_file = os.path.join(temp_output_path, f'test_{module_name}.py')
            if os.path.exists(generated_test_file):
                new_test_file_path = None
                existing_pynguin_test_files = glob.glob(os.path.join(project_path, f'test_{module_name}_pynguin_*.py'))
                if len(existing_pynguin_test_files) > 0:
                    new_test_file_path = os.path.join(project_path, f'test_{module_name}_pynguin_{len(existing_pynguin_test_files)}.py')
                else:
                    new_test_file_path = os.path.join(project_path, f'test_{module_name}_pynguin_0.py')
                shutil.copy(generated_test_file, new_test_file_path)

                public_test_file_path = os.path.join(os.path.basename(project_path), os.path.basename(new_test_file_path))
                shutil.rmtree(temp_output_path, ignore_errors=True)  # Clean up the output directory
                return f"Pynguin ran successfully. Generated test file path: {public_test_file_path}"
            else:
                shutil.rmtree(temp_output_path, ignore_errors=True)
                return f"No test file generated by Pynguin. Maybe some error occured? Output:\n{result.stdout}{result.stderr}"
        else:
            shutil.rmtree(temp_output_path, ignore_errors=True)
            return f"Pynguin failed. Output:\n{result.stdout}{result.stderr}"
    except Exception as e:
        shutil.rmtree(temp_output_path, ignore_errors=True)
        return f"Error running Pynguin: {str(e)}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    
    # start_time = time.time()
    # print(run_pynguin('largest_prime_factor/largest_prime_factor.py'))
    # end_time = time.time()
    # print(f"Execution time: {end_time - start_time:.2f} seconds")