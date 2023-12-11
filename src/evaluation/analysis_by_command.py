import os
import subprocess
import time

def command_with_timeout(cmd, timeout=60):
    """
    Execute a command with a specified timeout.
    :param cmd: Command to be executed.
    :param timeout: Time (in seconds) after which the command will be terminated.
    :return: Standard output and standard error of the executed command.
    """
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    start_time = time.time()

    while True:
        if p.poll() is not None:
            break
        elapsed_time = time.time() - start_time
        if timeout and elapsed_time > timeout:
            p.terminate()
            return 'TIMEOUT', 'TIMEOUT'
        time.sleep(1)

    out, err = p.communicate()
    return out, err    


def compile_python(test_dir, name):
    """
    Compile a Python file using Pylint and return the output and error.
    :param test_dir: Directory containing the Python file.
    :param name: Name of the Python file without the extension.
    :return: Output and error of the compilation process.
    """
    generated_code_dir = test_dir
    cur_dir = os.getcwd()

    try:
        os.chdir(generated_code_dir)
        out, err = command_with_timeout(["pylint", name + ".py"], timeout=10)
        os.chdir(cur_dir)
        return out, err
    except Exception as e:
        print(e)
        os.chdir(cur_dir)
        return 'uncompilable', "uncompilable"


def run_pylint():
    """
    Run Pylint on generated Python files and save the output to text files.
    """
    code_dir = "path/to/data/results/code/python/"
    generated_report_dir = "path/to/data/results/reports/python/pylint/"

    if not os.path.exists(generated_report_dir):
        os.makedirs(generated_report_dir)

    for file in os.listdir(code_dir):
        if file.endswith(".py"):
            name = file.split(".")[0]
            out, err = compile_python(code_dir, name)
            with open(generated_report_dir + name + ".txt", "w") as f:
                f.write(out)


def run_flake8_python():
    """
    Run flake8 on generated Python files and save the output to text files.
    """
    code_dir = "path/to/data/results/code/python/"
    generated_report_dir = "path/to/data/results/reports/python/flake8/"

    if not os.path.exists(generated_report_dir):
        os.makedirs(generated_report_dir)

    for file in os.listdir(code_dir):
        if file.endswith(".py"):
            name = file.split(".")[0]
            out, err = command_with_timeout(["flake8", code_dir + file], timeout=10)
            with open(generated_report_dir + name + ".txt", "w") as f:
                f.write(out)


def run_pmd_java():
    """
    Run PMD on generated Java files and save the output to text files.
    """
    code_dir = "path/to/data/results/code/java/"
    generated_report_dir = "path/to/data/results/reports/java/pmd/"

    if not os.path.exists(generated_report_dir):
        os.makedirs(generated_report_dir)

    for file in os.listdir(code_dir):
        file_path = code_dir + file
        smell_txt = generated_report_dir + file + ".txt"
        os.system("pmd check -d {} -R rulesets/java/all.xml -f text -r {}".format(file_path, smell_txt))


def run_checkstyle_java():
    """
    Run Checkstyle on generated Java files and save the output to text files.
    """
    code_dir = "path/to/data/results/code/java/"
    generated_report_dir = "path/to/data/results/reports/java/checkstyle/"

    if not os.path.exists(generated_report_dir):
        os.makedirs(generated_report_dir)

    for file in os.listdir(code_dir):
        if file.endswith(".java"):
            file_path = code_dir + file
            smell_txt = generated_report_dir + file + ".txt"
            out, err = command_with_timeout(
                ["java", "-jar", "checkstyle/checkstyle-10.9.3-all.jar", "-c", "checkstyle/sun_checks.xml", file_path], 
                timeout=10
            )
            with open(smell_txt, "a") as f:
                f.write(str(out))

if __name__ == "__main__":
    run_pylint()
    run_flake8_python()
    run_pmd_java()
    run_checkstyle_java()

