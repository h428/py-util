import time

format_width_config = {
    'idx': 2,
    'pid': 8,
    'name': 10,
    'user': 8,
    'status': 10,
    'cpu': 8,
    'memory': 10,
    'gid': 6,
    'gpu': 8,
    'create_time': 22,
    'run_time': 10,
}

def format_memory(memory_mb):
    line = ""
    if memory_mb < 1024:
        line = f"{memory_mb}M"
    
    m = memory_mb / 1024
    line = f"{m:.2f}G"
    return line.rjust(format_width_config["memory"])


def format_runtime(create_time):

    run_time = time.time() - create_time

    if run_time < 60:
        return f"{run_time:.2f} s"
    
    run_time = run_time / 60
    if run_time < 60:
        return f"{run_time:.2f} m"
    
    run_time = run_time / 60
    if run_time < 24:
        return f"{run_time:.2f} h"
    
    return f"{run_time / 24:.2f} d"

def format_process(process, idx):
    idx = str(idx).rjust(format_width_config['idx'])
    pid = str(process.pid).rjust(format_width_config['pid'])
    name = str(process.name).rjust(format_width_config['name'])
    user = str(process.user).rjust(format_width_config['user'])
    status = str(process.status).rjust(format_width_config['status'])
    cpu_usage = (str(process.cpu_usage) + '%').rjust(format_width_config['cpu'])
    memory = format_memory(process.memory_mb)
    gpu_id = str(process.gpu_id).rjust(format_width_config['gid'])
    gpu_usage = str(str(process.gpu_usage) + '%').rjust(format_width_config['gpu'])
    gpu_mem = format_memory(process.gpu_mb)
    create_time = process.format_time.rjust(format_width_config['create_time'])
    run_time = format_runtime(process.create_time).rjust(format_width_config['run_time'])
    return f"{idx}{pid}{name}{status}{user}{cpu_usage}{memory}{gpu_id}{gpu_usage}{gpu_mem}{create_time}{run_time}"


def format_process_list(process_list):
    print()
    # 标题对齐
    idx = '-'.rjust(format_width_config['idx'])
    pid = 'pid'.rjust(format_width_config['pid'])
    name = 'name'.rjust(format_width_config['name'])
    user = 'user'.rjust(format_width_config['user'])
    status = 'status'.rjust(format_width_config['status'])
    cpu_usage = 'cpu'.rjust(format_width_config['cpu'])
    memory = 'memory'.rjust(format_width_config['memory'])
    gpu_id = 'gid'.rjust(format_width_config['gid'])
    gpu_usage = 'gpu'.rjust(format_width_config['gpu'])
    gpu_mem = 'gpu mem'.rjust(format_width_config['memory'])
    create_time = 'create time'.rjust(format_width_config['create_time'])
    run_time = 'run time'.rjust(format_width_config['run_time'])
    print(f"{idx}{pid}{name}{status}{user}{cpu_usage}{memory}{gpu_id}{gpu_usage}{gpu_mem}{create_time}{run_time}")
    for idx, process in enumerate(process_list):
        print(format_process(process, idx))
    print()