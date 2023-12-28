import os
import psutil

# 获取当前电脑上正在运行的进程信息
process_info = psutil.process_iter()

# 遍历进程信息并打印进程名称和PID
for process in process_info:
    print(f"{process.name()} (PID: {process.pid})")

# 指定要打开的应用名称
app_to_open = input("请输入要打开的应用名称：")

# 遍历进程信息，查找并打开指定的应用
for process in process_info:
    if process.name() == app_to_open:
        # 获取应用的路径
        app_path = process.exe()

        # 打开应用
        os.startfile(app_path)

        # 退出循环
        break
