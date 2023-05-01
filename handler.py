from librarymanager import run_command
def install_lib(lib_name):
    return_code = run_command(f"pip install {lib_name}")
    return return_code

def uninstall_lib(lib_name):
    return_code = run_command(f"pip uninstall {lib_name} -y")
    return return_code

def upgrade_lib(lib_name):
    return_code = run_command(f"pip install {lib_name} --upgrade")
    return return_code

def search_lib(lib_name):
    return_code = run_command(f"pip search {lib_name}")
    return return_code  

def load_libs():
    log = run_command("pip freeze")
    # with open("libs.txt", "r") as file:
    #     libs = file.read()
    return log

