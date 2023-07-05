from process import Process
from cmds import kill_process_by_pid
from formater import format_process_list, format_process


def main():

    lines = [
        "请输入指令：",
        "1. 按 MEM 查询",
        "2. 按 GPU 查询",
        "-. kill id, cmd id",
    ]
    text = "\n".join(lines) + "\n"

    process_list = []
    while True:

        line = input(text)

        if line.startswith("q"):
            break

        if line.startswith("1"):
            process_list = Process.get_process_list_by_memory()
            format_process_list(process_list)
            continue

        if line.startswith("2"):
            process_list = Process.get_process_list_by_gpu()
            format_process_list(process_list)
            continue

        if line.startswith("kill"):
            no = int(line.replace("kill", "").strip())
            if no >= len(process_list):
                print("进程不存在\n")
                continue

            process = process_list[no]
            confirm = input(f"{format_process(process, no)}\n确认杀死上述进程？(yes) ")

            if confirm.startswith("y"):
                kill_process_by_pid(process['pid'])
            continue

        print("非法指令...")
     

if __name__ == '__main__':
    main()