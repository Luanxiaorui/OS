import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from entity.process import Process
from control.scheduler import Scheduler


class ProcessManagerGUI:

    process_que = []
    running = False
    q = 1

    def __init__(self, root):
        self.root = root
        self.root.title("进程管理模拟器")

        # 初始化调度器
        self.scheduler = Scheduler()

        # 进程计数, 分配PID
        self.process_count = 1

        # 创建GUI组件
        self.create_widgets()


    def create_widgets(self):
        # “添加进程”框架
        add_frame = ttk.LabelFrame(self.root, text="添加进程")
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(add_frame, text="进程名称:").grid(row=0, column=0, padx=5, pady=5)
        self.pname_entry = ttk.Entry(add_frame)
        self.pname_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="到达时间:").grid(row=1, column=0, padx=5, pady=5)
        self.arrival_entry = ttk.Entry(add_frame)
        self.arrival_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="执行时间:").grid(row=2, column=0, padx=5, pady=5)
        self.burst_entry = ttk.Entry(add_frame)
        self.burst_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="优先级(nice值):").grid(row=3, column=0, padx=5, pady=5)
        self.priority_entry = ttk.Entry(add_frame)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(add_frame, text="添加进程", command=self.add_process)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=5)

        # 控制框架
        control_frame = ttk.LabelFrame(self.root, text="控制")
        control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.start_button = ttk.Button(control_frame, text="开始运行", command=self.start_running)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.next_button = ttk.Button(control_frame, text="下一时刻", command=self.next_step)
        self.next_button.grid(row=0, column=1, padx=5, pady=5)

        self.run_one = ttk.Button(control_frame, text="一次运行", command=self.run_thread)
        self.run_one.grid(row=0, column=2, padx=5, pady=5)

        # 调度算法选择
        ttk.Label(control_frame, text="调度算法:").grid(row=1, column=0, padx=5, pady=5)
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("FCFS")
        self.algorithm_menu = ttk.OptionMenu(control_frame, self.algorithm_var, "FCFS", "FCFS", "CFS", "RR")
        self.algorithm_menu.grid(row=1, column=1, padx=5, pady=5)

        # 进程控制框架
        manage_frame = ttk.LabelFrame(self.root, text="进程控制")
        manage_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(manage_frame, text="PID:").grid(row=0, column=0, padx=5, pady=5)
        self.control_pid_entry = ttk.Entry(manage_frame)
        self.control_pid_entry.grid(row=0, column=1, padx=5, pady=5)

        self.block_button = ttk.Button(manage_frame, text="阻塞进程", command=self.block_process)
        self.block_button.grid(row=1, column=0, padx=5, pady=5)

        self.wakeup_button = ttk.Button(manage_frame, text="唤醒进程", command=self.wakeup_process)
        self.wakeup_button.grid(row=1, column=1, padx=5, pady=5)

        self.revoke_button = ttk.Button(manage_frame, text="撤销进程", command=self.revoke_process)
        self.revoke_button.grid(row=2, column=0, padx=2, pady=5)

        self.clear_button = ttk.Button(manage_frame, text="清除进程", command=self.clear_process)
        self.clear_button.grid(row=2, column=1, padx=2, pady=5)

        # 进程列表显示
        list_frame = ttk.LabelFrame(self.root, text="进程列表")
        list_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

        columns = ("PID", "进程名称",'优先级', "到达时间", "执行时间", "剩余时间", "状态", "当前运行时刻")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill='both', expand=True)

        # 周转时间显示框架
        metrics_frame = ttk.LabelFrame(self.root, text="运行结果")
        metrics_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.metrics_text = tk.Text(metrics_frame, height=10, width=80, state='disabled')
        self.metrics_text.pack(fill='both', expand=True)


    def get_val(self):
        # 弹出输入框，要求用户输入一个数字
        user_input = simpledialog.askstring("输入", "请输入一个数字:")

        # 如果用户输入了内容，尝试将其转换为数字
        if user_input is not None:
            try:
                number = float(user_input)
                return number
            except ValueError:
                messagebox.showerror("wrong", "你输入的不是数字， 时间片将默认为1")
                return 1
        else:
            messagebox.showerror("wrong", "你输入的不是数字， 时间片将默认为1")
            return 1

    def clear_process(self):
        self.process_que.clear()

    def add_process(self):
        try:
            pid = self.get_pid()
            pname = self.pname_entry.get().strip()
            arrival_time = int(self.arrival_entry.get().strip())
            burst_time = int(self.burst_entry.get().strip())
            priority = 0 if self.priority_entry.get().strip() == '' else int(self.priority_entry.get().strip())

            if not pid:
                raise ValueError("内容不能为空")
            self.process_que.append(Process(PID=pid, Pname= pname, arriveTime=arrival_time, needtime=burst_time, pri=priority))
            self.update_process_list()
            # 清空输入框
            self.pname_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        except ValueError as ve:
            messagebox.showerror("输入错误", str(ve))


    def start_running(self): # 开始运行
        if self.process_que is None or len(self.process_que) == 0:
            messagebox.showerror("错误", "进程队列为空")
            return
        if self.running:
            return

        self.running = True

        # 切换使用的调度算法
        use_algorithm = self.algorithm_var.get()
        time_part = 1
        if use_algorithm == 'RR':
            time_part = self.get_val()

        print(use_algorithm)
        self.scheduler = Scheduler(use_algorithm, time_part)

        # 将进程放入就绪队列
        for process in self.process_que:
            self.scheduler.add_process(process)
        messagebox.showinfo("准备就绪", "可以开始运行")

    def next_step(self):# 运行一个时间片
        if not self.running:
            return
        if self.scheduler.run_one_step():
            self.display_metrics()
            self.running = False
        self.update_process_list()

    def run_thread(self):
        if not self.running: # 只有点了开始运行，为运行态才运行
            return
        run = threading.Thread(target=self.next_one_step) # 创建运行一步的线程
        run.start()

    def next_one_step(self):# 运行一个时间片，“一次运行”中使用
        while True:
            if self.q == 1: # 只有信号量为1,才能运行
                f = self.scheduler.run_one_step() # 运行一个时间片
                self.update_process_list() # 刷新
                self.q = 1 # 释放信号量
                if f:
                    self.display_metrics() # 展示运行情况
                    self.running = False  # 运行结束，停止运行
                else:
                    time.sleep(1) # 停一秒，模拟时间消耗
                    self.run_thread() # 未运行结束，继续运行
                break


    def block_process(self):# 阻塞进程
        if not self.running:
            return
        self.q = 0   # 抢占信号量
        time.sleep(0.2)  # 避免同时操作heapq，保证时间片运行完整
        if len(self.control_pid_entry.get()) > 0:
            PID = self.control_pid_entry.get()
            self.scheduler.stop(PID)
            self.update_process_list()
            self.q = 1  # 释放信号量


    def wakeup_process(self): # 唤醒进程
        if not self.running:
            return
        self.q = 0
        time.sleep(0.2)
        if len(self.control_pid_entry.get()) > 0:
            PID = self.control_pid_entry.get()
            self.scheduler.wakeup(PID)
            self.update_process_list()
            self.q = 1  # 释放


    def revoke_process(self): # 撤销进程
        if not self.running:
            return
        self.q = 0
        time.sleep(0.2)
        if len(self.control_pid_entry.get()) > 0:
            PID = self.control_pid_entry.get()
            self.scheduler.remove_process(PID)
            self.update_process_list()
            self.q = 1  # 释放

    def update_process_list(self):
        # 清空树视图
        for item in self.tree.get_children():
            self.tree.delete(item)
        # 添加所有进程到树视图
        vals =  self.scheduler.sche.get_all_process() if self.running else self.process_que
        for process in vals:
            # if type(process) is tuple:
            #     process = process[1]
            self.tree.insert('', tk.END, values=(
                process.pid,
                process.Pname,
                process.priority,
                process.arriveTime,
                process.runtime,
                process.needTime,
                process.state,
                self.scheduler.T
            ))

    def display_metrics(self):
        total_turnaround_time = 0
        total_weighted_turnaround_time = 0
        metrics = []
        # print(666)
        for process in self.scheduler.sche.finishedList:
            turnaround_time = process.endTime - process.arriveTime
            weighted_turnaround_time = turnaround_time / process.runtime
            total_turnaround_time += turnaround_time
            total_weighted_turnaround_time += weighted_turnaround_time
            metrics.append(f"进程 {process.pid}:\n"
                           f"进程名称 {process.Pname}\n"
                           f"  到达时间: {process.arriveTime}\n"
                           f"  运行时间: {process.runtime}\n"
                           f"  开始时间：{process.startTime}\n"
                           f"  完成时间: {process.endTime}\n"
                           f"  周转时间: {turnaround_time}\n"
                           f"  带权周转时间: {weighted_turnaround_time:.2f}\n")

        average_turnaround_time = total_turnaround_time / len(self.scheduler.sche.finishedList)
        average_weighted_turnaround_time = total_weighted_turnaround_time / len(self.scheduler.sche.finishedList)

        metrics.append(f"平均周转时间: {average_turnaround_time:.2f}\n")
        metrics.append(f"平均带权周转时间: {average_weighted_turnaround_time:.2f}\n")

        # 显示在metrics_text控件中
        self.metrics_text.config(state='normal')
        self.metrics_text.delete('1.0', tk.END)
        self.metrics_text.insert(tk.END, "\n".join(metrics))
        self.metrics_text.config(state='disabled')
        messagebox.showinfo("运行结束", "所有进程已完成运行，周转时间和带权周转时间已计算。")

    def get_pid(self):
        pid = str(self.process_count)
        while len(pid) < 5:
            pid = '0' + pid
        self.process_count += 1
        return pid

def main():
    root = tk.Tk()
    ProcessManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()