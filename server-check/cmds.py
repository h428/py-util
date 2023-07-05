import os
import re
import subprocess
from formater import format_process_list

def kill_process_by_pid(pid):
    os.system(f"sudo kill -9 {pid}")

def get_pid_list_by_memory():
    command = "ps aux | awk '$6>=1024000'"
    output = subprocess.check_output(command, shell=True).decode("utf-8")
    process_pattern = r"\w+\s+(\d+)\s+.+\n"
    matches = re.findall(process_pattern, output)

    pid_list = [int(pid) for pid in matches]

    return pid_list


if __name__ == "__main__":
    print(get_pid_list_by_memory())