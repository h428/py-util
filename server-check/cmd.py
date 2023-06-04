import os
import re
import subprocess
import psutil
from formater import format_process_list


def get_process_info(pid):
    process = psutil.Process(pid)

    username = process.username()
    cpu_percent = process.cpu_percent(interval=0.1)
    memory_info = process.memory_info()
    uptime = process.create_time()
    cmd = process.cmdline()

    # 获取内存占用的字节数，并转换为MB
    memory_usage = memory_info.rss / 1024 / 1024

    return username, cpu_percent, memory_usage, uptime, cmd

def parse_nvidia_smi_output(output):
    gpu_pattern = r"(\d+)MiB\s+/\s+(\d+)MiB\s+\|\s+(\d+)%"
    gpu_info_list = re.findall(gpu_pattern, output)
    gpu_used_list = [int(x[2]) for x in gpu_info_list]

    # 定义用于提取进程信息的正则表达式模式
    process_pattern = r"\|\s+(\d)\s+N/A\s+N/A\s+(\d+)\s+C\s+([\w\d/\.]+)\s+(\d+)MiB\s+\|"
    matches = re.findall(process_pattern, output)

    process_list = []
    for match in matches:
        gpu_id, pid, process_name, gpu_memory = match
        gpu_id = int(gpu_id)
        pid = int(pid)
        gpu_memory = float(gpu_memory)
        gpu_used = gpu_used_list[gpu_id]
        user, cpu_used, memory, uptime, cmd = get_process_info(pid)
        process_list.append({
            'pid': pid,
            'user': user,
            'cpu_used': cpu_used,
            'memory': memory,
            'gpu_id': gpu_id,
            'gpu_used': gpu_used,
            'gpu_memory': gpu_memory,
            'uptime': uptime,
            'cmd': cmd
        })

    return process_list

def nvidia_smi():
    output = subprocess.check_output(['nvidia-smi']).decode('utf-8')
    process_list = parse_nvidia_smi_output(output)
    return process_list


def kill_process_by_pid(pid):
    os.system(f"sudo kill -9 {pid}")

if __name__ == "__main__":
    process_list = nvidia_smi()
    format_process_list(process_list)