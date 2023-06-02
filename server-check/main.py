from cmd import nvidia_smi
from formater import format_process_list, format_process


def main():

    lines = [
        "请输入指令：",
        "1. 按 GPU 查询",
        "2. 按 CPU 查询",
        "-. kill id",
    ]
    text = "\n".join(lines) + "\n"

    process_list = []
    while True:

        line = input(text)

        if line.startswith("q"):
            break

        if line.startswith("1"):
            continue

        if line.startswith("2"):
            process_list = nvidia_smi()
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
                print("杀死进程")
            continue

        print("非法指令...")
     

if __name__ == '__main__':
    main()