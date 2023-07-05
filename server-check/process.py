import psutil
import time
from datetime import datetime
import math
from gpus import get_plain_process_list_by_gpu
from cmds import get_pid_list_by_memory
from formater import format_process_list

class Process:
    def __init__(self, pid, name, status, user, create_time, cpu_usage, memory_bytes, gpu_id=-1, gpu_usage=0, gpu_mb=0):
        self.pid = pid # pid
        self.name = name # 启动命令的名称
        self.status = status  # 状态，stopped 和 zombie 表示可以 kill
        self.user = user  # 归属用户
        self.create_time = create_time
        self.cpu_usage = cpu_usage  # cpu 利用率
        self.memory_bytes = memory_bytes  # 占用的 rss 物理内存字节数
        self.gpu_id = gpu_id # 占用的 gpu 编号，从 0 开始
        self.gpu_usage = gpu_usage # gpu 利用率（当前卡的）
        self.gpu_mb = gpu_mb  # 占用 gpu 显存大小，单位为 MB

        # 辅助字段
        self.memory_mb = math.ceil(memory_bytes / 1024 / 1024)
        self.format_time = datetime.fromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")

    def __eq__(self, other):
        if isinstance(other, Process):
            return self.pid == other.pid
        return False

    def __hash__(self):
        return hash((self.pid))

    def __str__(self):
        return f'Process(pid={self.pid}, name={self.name}, status={self.status}, user={self.user}, created_time={self.format_time}' \
            + f', cpu_usage={self.cpu_usage}, memory_bytes={self.memory_bytes}, gpu_id={self.gpu_id}, gpu_usage={self.gpu_usage}, gpu_mb={self.gpu_mb})'

    def is_zombie(self):
        run_time = time.time() - self.create_time
        if not self.status == 'running' and self.cpu_usage == 0 and self.gpu_usage == 0 and run_time > 60:
            return True
        return False
    
    def not_zombie(self):
        return not self.is_zombie()

    def find_process_by_pid(process_list, pid):
        return next((p for p in process_list if p.pid == pid), None)

    @staticmethod
    def get_by_pid(pid, gpu_id=-1, gpu_usage=0, gpu_mb=0):
        try:
            p = psutil.Process(pid)
            pid = p.pid
            name = p.name()
            status = p.status()
            user = p.username()
            create_time = p.create_time()
            cpu_usage = math.ceil(p.cpu_percent(0.1))  # 统计 cpu 利用率的间隔为 0.2 秒，上取整为整数
            memory_bytes = p.memory_info().rss
            return Process(pid, name, status, user, create_time, cpu_usage, memory_bytes, gpu_id, gpu_usage, gpu_mb)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
        
    @staticmethod
    def get_process_list_by_gpu():
        plain_gpu_process_list = get_plain_process_list_by_gpu()
        gpu_list = [Process.get_by_pid(plain_process["pid"], plain_process["gpu_id"], plain_process["gpu_usage"], plain_process["gpu_mb"]) for plain_process in plain_gpu_process_list]
        return gpu_list
    
    @staticmethod
    def get_process_list_by_memory():
        pid_list = get_pid_list_by_memory()
        memory_list = [Process.get_by_pid(pid) for pid in pid_list]
        return memory_list
    
    @staticmethod
    def get_zombie_process_list():
        gpu_list = Process.get_process_list_by_gpu()
        memory_list = Process.get_process_list_by_memory()
        merged_list = list(set(gpu_list + memory_list))
        zombie_list = [p for p in merged_list if p.is_zombie()]

        return zombie_list


    @staticmethod
    def get_all_processes():
        processes = []
        for pid in psutil.pids():
            p = Process.get_by_pid(pid)
            if p:
                process.append(p)
        return processes

if __name__ == "__main__":
    all_processes = Process.get_zombie_process_list()
    for process in all_processes:
        print(process)
    format_process_list(all_processes)
    