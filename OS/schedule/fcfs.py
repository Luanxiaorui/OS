import heapq
from entity.process import Process
from entity.sche import Schedule

class FCFS(Schedule):

    def __init__(self):
        super().__init__()
        self.not_arrived = []  # 还未到达的进程列表
        self.readyQue = []
        self.blockList = []  # 阻塞队列
        self.finishedList = []  # 完成队列
        self.current_process = None  # 当前运行的进程
        self.T = 0  # 当前时间

    def add_process(self, process: Process):
        """
        添加一个新的进程到调度器。
        """
        self.not_arrived.append(process)

    def remove_process(self, pid):
        """
        根据 PID 移除一个进程，可能在就绪队列、阻塞队列或完成队列中。
        """
        for queue in [self.not_arrive, self.blockList]:
            pro = next((p for p in queue if p.pid == pid), None)
            if pro:
                queue.remove(pro)
                break
        for item in self.readyQue:
            if item[1].pid == pid:
                self.readyQue.remove(item)
                break

        # 尝试从当前运行的进程中移除
        if self.current_process and self.current_process.PID == pid:
            self.current_process = None
            return True
        return False  # 如果没有找到进程

    def get_next_process(self):
        """
        获取下一个要运行的进程。
        """
        if self.readyQue:
            priority, pro = heapq.heappop(self.readyQue)
            pro.state = 'RUNNING'
            return pro

    def run_one_step(self):
        """
        运行一个时间片（1个单位时间）。
        """
        # 1. 将到达时间为当前时间的进程加入就绪队列
        for pro in self.not_arrived:
            if pro.arriveTime <= self.T:
                pro.state = 'READY'
                heapq.heappush(self.readyQue, (max(pro.arriveTime, pro.wakeTime), pro))
                self.not_arrived.remove(pro)

        # 2. 如果没有当前运行的进程，获取下一个进程
        if self.current_process is None:
            self.current_process = self.get_next_process()
            if self.current_process:
                if self.current_process.startTime == -1:
                    self.current_process.startTime = self.T  # 记录实际开始时间
                self.current_process.setStatus('RUNNING')  # 设置为运行状态

        # 3. 运行当前进程
        if self.current_process:
            self.current_process.runtime += 1
            self.current_process.needTime -= 1

            # 检查进程是否完成
            if self.current_process.needTime == 0:
                self.current_process.endTime = self.T + 1  # 设置完成时间
                self.current_process.setStatus('FINISH')  # 设置为完成状态
                self.finishedList.append(self.current_process)
                self.current_process = None

        # 4. 增加时间
        self.T += 1
        return self.check_finish()

    def wakeup(self, pid):
        """
        唤醒一个被阻塞的进程。
        """
        for pro in self.blockList:
            if pro.PID == pid:
                self.blockList.remove(pro)
                heapq.heappush(self.readyQue, (max(pro.arriveTime, pro.wakeTime), pro))
                pro.setStatus('READY')  # 设置为就绪状态
                return True
        return False  # 如果没有找到进程

    def stop(self, pid):
        """
        阻塞一个正在运行的进程
        """
        if self.current_process and self.current_process.pid == pid:
            self.current_process.setStatus('BLOCK')  # 设置为阻塞状态
            # self.current_process.wakeTime = self.T + wake_time  # 设置唤醒时间
            self.blockList.append(self.current_process)
            self.current_process = None
            return True
        return False  # 如果没有找到进程或当前没有运行的进程

    def get_all_process(self):
        """
        获取所有进程，包括未到达、就绪、阻塞和完成的进程。
        """
        all_processes = self.not_arrived + [item[1] for item in self.readyQue] + self.blockList + self.finishedList
        if self.current_process:
            all_processes.append(self.current_process)
        return all_processes

    def check_finish(self):
        return len(self.readyQue) == 0 and len(self.not_arrived) == 0 and len(self.blockList) == 0 and self.current_process is None

