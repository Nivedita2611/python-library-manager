from librarymanager import run_command
import requests
import json
def inlib(lib_name):
    return_code = run_command(f"pip install {lib_name}")
    return return_code

def unlib(lib_name):
    return_code = run_command(f"pip uninstall {lib_name} -y")
    return return_code

def uplib(lib_name):
    return_code = run_command(f"pip install {lib_name} --upgrade")
    return return_code

def search_lib(lib_name):

    # Define search parameters
    search_term = lib_name
    search_url = f'https://pypi.org/pypi/{search_term}/json'

    # Send GET request and parse response as JSON
    response = requests.get(search_url)
    response_json = json.loads(response.text)

    # Retrieve package metadata
    name = response_json['info']['name']
    version = response_json['info']['version']
    summary = response_json['info']['summary']

    details = [name , version, summary]
    return details

def load_libs():
    log = run_command("pip freeze")
    # with open("libs.txt", "r") as file:
    #     libs = file.read()
    return log

