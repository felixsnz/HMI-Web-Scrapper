
import subprocess
from utils.logger import get_logger

def run_bash_script(script_path):
    try:
        subprocess.run(['bash', script_path], check=True)
        print(f'Script {script_path} ran successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Script {script_path} failed. Return code was: {e.returncode}')