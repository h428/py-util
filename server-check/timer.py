from datetime import datetime
import time
import sys
from cmds import kill_process_by_pid
from formater import format_process_list
from process import Process

if __name__ == "__main__":
    while True:
        now = datetime.now()
        print(f"{now.strftime('%Y-%m-%d %H:%M:%S')} 执行内鬼进程检查...")
        zombie_list = Process.get_zombie_process_list()
        
        if len(zombie_list) == 0:
            print("本次未检测到内鬼进程...")
            sys.stdout.flush()
            time.sleep(3600)  # 一小时执行一次
            continue

        print("本次检测到内鬼进程列表如下：")
        format_process_list(zombie_list)

        count_time = 10
        for zombie in zombie_list:
            zombie_recheck = True
            # 对该僵尸进程查询 10 次
            for i in range(count_time):
                # 休眠一秒
                time.sleep(1)
                new_zombie_list = Process.get_zombie_process_list()
                found = Process.find_process_by_pid(new_zombie_list, zombie.pid)

                # 新列表没找到，说明首次查询是误判
                if not found or found.not_zombie():
                    print(f"第 {i+1} 次轮询时发现 {zombie.pid} 不是内鬼...")
                    print(f"首次被误判为内鬼时的对象信息为：{zombie}")
                    if found:
                        print(f"本次轮询查到的最新信息为：{found}")
                    else:
                        print(f"但本次没有在僵尸进程列表中找到上述进程")
                
                    zombie_recheck = False
                    break
            
            if zombie_recheck == False:
                continue

            print(f"经过 {count_time} 次连续查询后，发现 {zombie.pid} 仍是内鬼，即将杀死！！！")
            kill_process_by_pid(zombie.pid)
            print(f"成功杀死内鬼：{zombie}")

        print("本次内鬼检查执行结束...")
        sys.stdout.flush()
        time.sleep(3600)  # 一小时执行一次