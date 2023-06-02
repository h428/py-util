def format_memory(memory):
    if memory < 1024:
        return f"{memory:9.2f}M"
    
    m = memory / 1024
    return f"{m:9.2f}G"


def format_process(process_item, idx):
    pid = process_item['pid']
    user = process_item['user']
    cpu_used = process_item['cpu_used']
    memory = process_item['memory']
    gpu_id = process_item['gpu_id']
    gpu_used = process_item['gpu_used']
    gpu_memory = process_item['gpu_memory']
    gpu_info = f"{gpu_id}/{gpu_used}"
    return f"{idx:2d}{pid:8d}{user.rjust(6)}{cpu_used:10.2f}{format_memory(memory)}{gpu_info.rjust(10)}{format_memory(gpu_memory)}"


def format_process_list(process_list):
    print()
    print(f"{'-'.rjust(2)}{'pid'.rjust(8)}{'user'.rjust(6)}{'cpu used'.rjust(10)}{'memory'.rjust(10)}{'gpu used'.rjust(10)}{'gpu mem'.rjust(10)}")
    for idx, process in enumerate(process_list):
        print(format_process(process, idx))
    print()