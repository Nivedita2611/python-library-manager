import subprocess
from datetime import datetime


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
    log(message, "success")

def log_error(message):
    log(message, "error")


def log(message, state):
    filewithdate = "log"+datetime.now().strftime("%Y_%m_%d") + ".txt"
    with open(filewithdate, "a") as log_file:
        log_file.write(f"{datetime.now()}| {state} | {message}\n")

def run_command(command):
    cmd_list = command_string_to_list(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if get_returncode_text(result.returncode) == "Success":
        output = result.stdout.strip()
        log_success(output)
        print("Success")
    else:
        error = result.stderr.strip()
        log_error(error)
        print("Error")
    return result.returncode



return_code = run_command("pip install scikit-learn")
print(return_code)
