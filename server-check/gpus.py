import os
import re
import subprocess

def find_plain_gpu_process_by_pid(plain_process_list, pid):
    return next((p for p in plain_process_list if p["pid"] == pid), None)

def parse_nvidia_smi_output(output):
    # 获取各个 gpu 的使用率 volatile
    gpu_pattern = r"(\d+)MiB\s+/\s+(\d+)MiB\s+\|\s+(\d+)%"
    gpu_info_list = re.findall(gpu_pattern, output)
    gpu_usage_list = [int(x[2]) for x in gpu_info_list]

    # 定义用于提取占用了显存的进程信息的正则表达式模式
    process_pattern = r"\|\s+(\d)\s+N/A\s+N/A\s+(\d+)\s+C\s+([\w\d/\.]+)\s+(\d+)MiB\s+\|"
    matches = re.findall(process_pattern, output)

    plain_gpu_process_list = []
    for match in matches:
        gpu_id, pid, process_name, gpu_mb = match

        gpu_id = int(gpu_id)
        pid = int(pid)
        gpu_mb = int(gpu_mb)
        gpu_usage = gpu_usage_list[gpu_id]

        plain_gpu_process = {"pid":pid, "gpu_id":gpu_id, "gpu_usage":gpu_usage, "gpu_mb":gpu_mb}

        # 处理单进程多卡情况，选取最大的那个值存储下来
        found_process = find_plain_gpu_process_by_pid(plain_gpu_process_list, pid)
        if found_process:
            # 以计算量为标准，若在这张卡计算量更大，将显卡相关值替换为这张卡
            if gpu_usage > found_process["gpu_usage"]:
                found_process["gpu_mb"] = gpu_mb
                found_process["gpu_id"] = gpu_id
                found_process["gpu_usage"] = gpu_usage
            # 单卡多进程，无需再次 append，直接 continue
            continue

        plain_gpu_process_list.append(plain_gpu_process)

    return plain_gpu_process_list

def get_plain_process_list_by_gpu():
    output = subprocess.check_output(['nvidia-smi']).decode('utf-8')
    plain_process_list = parse_nvidia_smi_output(output)
    return plain_process_list


if __name__ == "__main__":
    ps = get_plain_process_list_by_gpu()
    for p in ps:
        print(p)