import tkinter as tk
from threading import Thread
import time

# 执行的任务1
def task1():
    for i in range(10):
        print(f"任务1执行中：{i}")
        time.sleep(1)  # 模拟耗时操作

# 执行的任务2
def task2():
    for i in range(10):
        print(f"任务2执行中：{i}")
        time.sleep(1)  # 模拟耗时操作

# 启动线程执行任务1
def run_task1():
    thread1 = Thread(target=task1)  # 创建线程
    thread1.start()                # 启动线程

# 启动线程执行任务2
def run_task2():
    thread2 = Thread(target=task2)  # 创建线程
    thread2.start()                # 启动线程

# 创建窗口
root = tk.Tk()
root.title("多线程窗体示例")
root.geometry("300x200")

# 添加按钮
button1 = tk.Button(root, text="执行任务1", command=run_task1)
button1.pack(pady=20)

button2 = tk.Button(root, text="执行任务2", command=run_task2)
button2.pack(pady=20)

# 运行主循环
root.mainloop()
