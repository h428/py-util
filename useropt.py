#!/opt/anaconda3/bin python
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import pwd
import shutil
from datetime import datetime

# 待执行的命令
useradd_cmd = "sudo useradd -M -d /home/{username} -s /bin/bash {username}"
create_user_data_folder_cmd = "sudo mkdir -m 755 {user_data_path} && sudo chown {username}:{username} {user_data_path}"
create_link_cmd = "sudo ln -s {user_data_path} /home/{username}"
change_pass_cmd = "echo \"{username}:{password}\" | sudo chpasswd"
change_own_and_perm = "sudo chmod {perm} {path} && sudo chown {username}:{username} {path}"
mkdir_cmd = "sudo -u {username} mkdir {path}"
copy_cmd = "sudo cp {from_path} {to_path}"
create_ssh_pair_cmd = "sudo ssh-keygen -t rsa -N \"\" -f {private_file_path} -q"
append_pub_cmd = "sudo cat {public_file_path} >> {authorized_keys_path}"


def user_exists(username):
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def execution(cmd):
    print("will execution: " + cmd)
    os.system(cmd)


def configure_ssh(username, user_data_path, home_path, args):

    # 提前准备相关路径
    ssh_path = os.path.join(home_path, ".ssh")
    input_public_file = args.public_file
    public_file_path = os.path.join(ssh_path, "id_rsa.pub")
    private_file_path = os.path.join(ssh_path, "id_rsa")
    authorized_keys_path = os.path.join(ssh_path, "authorized_keys")

    # 5. 设置免密登录（以 root 用户作为上下文进行设置，最后统一更换归属和权限）

    # 如果已存在 .ssh 目录和 authorized_keys 文件，则原来已经配置过 ssh，跳过配置
    if os.path.exists(ssh_path) and os.path.exists(authorized_keys_path):
        return

    # 5.1 确保 .ssh 目录存在且 root 可写
    if not os.path.exists(ssh_path):
        execution(mkdir_cmd.format(username="root", path=ssh_path))
        # 临时更改权限，用户后续脚本操作
        execution(change_own_and_perm.format(perm="777", username="root", path=ssh_path))

    # 5.2 如果指定了 pub 路径，确保公钥路径存在
    if args.public_file:
        # 有提供 pub 则拷贝公钥到 ~/.ssh
        if not os.path.exists(input_public_file):
            print(f"公钥文件 {input_public_file} 不存在，请检查输入")
        execution(copy_cmd.format(from_path=input_public_file, to_path=public_file_path))
    else:
        # 没有提供则使用 ssh-keygen 生成一对
        execution(create_ssh_pair_cmd.format(private_file_path=private_file_path))

    # 5.3 将 id_rsa.pub 的内容追加到 authorized_keys
    execution(append_pub_cmd.format(authorized_keys_path=authorized_keys_path, public_file_path=public_file_path))

    # 统一权限更改：
    # 主目录修改归属用户
    execution(change_own_and_perm.format(username=username, perm="755", path=user_data_path))
    # .ssh 目录和 authorized_keys 更改权限为符合 .ssh 要求
    execution(change_own_and_perm.format(username=username, perm="700", path=ssh_path))
    execution(change_own_and_perm.format(username=username, perm="600", path=authorized_keys_path))
    # 其他文件更改
    execution(change_own_and_perm.format(username=username, perm="644", path=public_file_path))  # 拷贝或生成的 id_rsa.pub
    # 如果是生成 id_rsa
    if not args.public_file:
        execution(change_own_and_perm.format(username=username, perm="700", path=private_file_path))


def main():
    parser = argparse.ArgumentParser(description="用户操作")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", help="创建用户")
    group.add_argument("-d", "--delete", action="store_true", help="删除用户")
    group.add_argument("-r", "--restore", action="store_true", help="恢复用户")
    group.add_argument("-l", "--link", action="store_true", help="创建链接")

    exist_c = "-c" in sys.argv or "--create" in sys.argv
    exist_d = "-d" in sys.argv or "--delete" in sys.argv
    exist_r = "-r" in sys.argv or "--restore" in sys.argv
    exist_l = "-l" in sys.argv or "--link" in sys.argv

    parser.add_argument("-u", "--username", required=exist_c or exist_d, help="用户名")
    parser.add_argument("-f", "--folder", required=exist_c or exist_r or exist_l, help="存放用户数据的目录")
    parser.add_argument("-p", "--public_file", help="公钥文件路径")

    args = parser.parse_args()
    home_folder = "/home/"
    username = args.username

    if args.create:
        print("本次创建用户")
        folder = args.folder
        home_path = os.path.join(home_folder, username)
        user_data_path = os.path.join(folder, username)
        password = f"{username}@dmci"

        # 1. 校验用户是否已存在
        if user_exists(username):
            print(f"用户 {username} 已存在，请先删除对应用户或采用别的用户名")
            return

        # 2. 校验 folder 是否存在
        if not os.path.exists(folder):
            print(f"用户数据目录 {folder} 不存在，请检查输入或创建对应目录")
            return

        # 2. 校验 folder 下是否已存在对应用户目录
        if os.path.exists(user_data_path):
            print(f"用户数据目录 {folder} 已存在对应文件夹 {user_data_path}")
            return

        # 3. 校验 HOME 下是否已存在对应目录或软链接文件
        if os.path.exists(home_path):
            print(f"用户目录下已存在对应目录或文件 {home_path}")
            return

        # 4. 全都校验通过，可以创建，将默认密码输出至用户目录下的 pass.txt
        execution(useradd_cmd.format(username=username, password=password))    # 创建用户
        execution(create_user_data_folder_cmd.format(user_data_path=user_data_path, username=username))  # 创建用户目录
        execution(create_link_cmd.format(user_data_path=user_data_path, username=username))  # 创建软链接
        execution(change_pass_cmd.format(username=username, password=password))  # 修改密码

        # 5. 配置 ssh
        configure_ssh(username, user_data_path, home_path, args)

    if args.restore:
        print("本次根据用户数据目录恢复链接和用户")
        user_data_path = args.folder

        # 读取擦混入的 user_data_path
        if not os.path.exists(user_data_path):
            print(f"路径 {user_data_path} 不存在，无法恢复")

        username = os.path.basename(user_data_path)  # 取最后一级作为用户名
        password = f"{username}@dmci"
        home_path = os.path.join(home_folder, username)

        # 确保用户名不被占用
        if user_exists(username):
            print(f"用户 {username} 已存在，和路径 {user_data_path} 冲突，无法恢复")
            return

        # 确保用户目录不被占用
        if os.path.exists(home_path):
            print(f"路径 {home_path} 已存在，无法恢复")
            return

        # 全都校验通过，可以创建
        execution(useradd_cmd.format(username=username, password=password))  # 创建用户
        execution(create_link_cmd.format(user_data_path=user_data_path, username=username))  # 创建软链接
        execution(change_pass_cmd.format(username=username, password=password))  # 修改密码

        # 配置 ssh
        configure_ssh(username, user_data_path, home_path, args)

    if args.delete:
        line = input(f"即将移除用户 {username}，确认？(yes/no)")
        if not line.startswith("y"):
            return

        home_path = os.path.join(home_folder, username)

        # 软链接存在或者目录存在才进行文件操作
        if os.path.exists(home_path):
            user_data_path = os.path.realpath(home_path)  # 根据软链接确定真实的用户数据目录
            os.remove(home_path)  # 移除软链接

            # 软链接指向的用户数据目录存在时才进行移动式删除
            if os.path.exists(user_data_path):
                parent_path = os.path.dirname(user_data_path)  # 确定用户数据目录的父目录

                # 确保 to-be-delete 存在，用于移动（不会真正删除）
                to_be_delete_path = os.path.join(parent_path, "to-be-delete")
                if not os.path.exists(to_be_delete_path):
                    os.mkdir(to_be_delete_path)

                now = datetime.now()
                formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
                deleted_path = os.path.join(to_be_delete_path, username + "_" + formatted_now)
                shutil.move(user_data_path, deleted_path)

                # 为了避免找不到被删除用户，追加日志到 root 用户下的 remove.log
                append_log_cmd = "sudo echo \"{log}\" >> /root/remove.log"
                log = f"移除用户 {username} : link={home_path}, user_data_path={user_data_path}, deleted_path={deleted_path}"
                execution(append_log_cmd.format(log=log))

        # 用户存在则删除用户，不存在则跳过
        if user_exists(username):
            user_del_cmd = f"sudo userdel {username}"
            assert 0 == os.system(user_del_cmd), "删除用户失败，请手动删除"

    if args.link:
        print("本次创建链接")
        user_data_path = args.folder

        # 读取擦混入的 user_data_path
        if not os.path.exists(user_data_path):
            print(f"路径 {user_data_path} 不存在，无法恢复")

        username = os.path.basename(user_data_path)  # 取最后一级作为用户名
        home_path = os.path.join(home_folder, username)
        print("username", username)
        print("home_path", home_path)

        # 目录已存在，询问是否覆盖
        print("os.path.exists(home_path) ", os.path.islink(home_path))
        if os.path.islink(home_path):
            line = input(f"路径 {home_path} 已存在，是否覆盖？(yes/no)")
            if not line.startswith("y"):
                return
            print(f"移除原有软链接 {home_path}")
            os.unlink(home_path)

        # 创建链接
        print(f"创建新软链接 {home_path} -> {user_data_path}")
        execution(create_link_cmd.format(user_data_path=user_data_path, username=username))  # 创建软链接


if __name__ == '__main__':
    main()

