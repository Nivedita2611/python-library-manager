import subprocess
from datetime import datetime
import requests


def get_returncode_text(returncode):
    if returncode == 0:
        return "Success"
    elif returncode == 1:
        return "General error"
    elif returncode == 2:
        return "Invalid usage"
    elif returncode == 3:
        return "Internal error"
    else:
        return "Unknown error"
    
def command_string_to_list(command_string):
    return command_string.split()

def log_success(message):
    return log(message, "success")

def log_error(message):
    return log(message, "error")


def log(message, state):
    filewithdate = "log"+datetime.now().strftime("%Y_%m_%d") + ".txt"
    with open(filewithdate, "w") as log_file:
        log_file.write(f"{datetime.now()}| {state} |\n---\n{message}")
    return filewithdate

def run_command(command):
    cmd_list = command_string_to_list(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if get_returncode_text(result.returncode) == "Success":
        output = result.stdout.strip()
        print("Success")
        log = log_success(output)
    else:
        error = result.stderr.strip()
        log = log_error(error)
        print("Error")
    return log

def get_library_info(name):
    pypi_url = f"https://pypi.org/pypi/{name}/json"
    response = requests.get(pypi_url)
    if response.status_code == 200:
        return dict(response.json())['info']
    else:
        return None

# return_code = run_command("pip install scikit-learn")
# print(return_code)
