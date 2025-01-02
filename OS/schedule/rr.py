import itertools
from typing import List
from entity.process import Process

class RR:
    def __init__(self, time_part=1):
        self.readyQue = []
        self.blockList = []
        self.finishedList = []
        self.not_arrive = []
        self.T = 0
        self.time_part = time_part

    def add_process(self, pro: Process):  # 加入一个进程
        if pro.arriveTime <= self.T:
            pro.state = 'READY'
            self.readyQue.append(pro)
        else:
            self.not_arrive.append(pro)

    def remove_process(self, PID):  # 移除一个进程
        for queue in [self.readyQue, self.blockList, self.not_arrive]:
            pro = next((p for p in queue if p.pid == PID), None)
            if pro:
                queue.remove(pro)
                break

    def get_next_process(self):  # 获得这一时刻要运行的进程
        for pro in self.not_arrive:
            if pro.arriveTime <= self.T:
                pro.state = 'READY'
                self.readyQue.append(pro)
                self.not_arrive.remove(pro)

        if self.readyQue:
            return self.readyQue.pop(0)
        return None

    def run_one_step(self) -> bool:  # 每次运行一个时间片, 运行结束返回True， 否则False
        pro: Process = self.get_next_process()
        if pro is not None:
            pro.state = 'RUNNING'
            if pro.startTime == -1:
                pro.startTime = self.T
            t = min(pro.needTime, self.time_part)
            pro.runtime += t
            pro.needTime -= t
            if pro.needTime > 0:
                    pro.state = 'READY'  # 设置为 READY
                    self.readyQue.append(pro)
            else:
                pro.state = 'FINISH'
                pro.endTime = self.T + t
                self.finishedList.append(pro)
        self.T += self.time_part

        # 确保至少有一个进程为 RUNNING 状态
        if len(self.readyQue) > 0:
            self.readyQue[0].state = 'RUNNING'

        return self.check_finish()

    def wakeup(self, PID):  # 唤醒进程
            for pro in self.blockList:
                if pro.pid == PID:
                    pro.state = 'READY'
                    self.readyQue.append(pro)
                    self.blockList.remove(pro)
                    break

    def stop(self, PID):  # 阻塞进程
            for pro in self.readyQue:
                if pro.pid == PID:
                    pro.state = 'BLOCK'
                    self.blockList.append(pro)
                    self.readyQue.remove(pro)
                    break

    def get_all_process(self) -> List[Process]:  # 得到所有的进程
            all_processes = list(itertools.chain(self.readyQue, self.blockList, self.finishedList, self.not_arrive))
            return all_processes

    def check_finish(self):
            return len(self.readyQue) == 0 and len(self.not_arrive) == 0 and len(self.blockList) == 0

    # 示例代码
if __name__ == "__main__":
        rr = RR(time_part=1)
        rr.add_process(Process(PID=1, Pname='Process1', arriveTime=0, needtime=3, pri=0))
        rr.add_process(Process(PID=2, Pname='Process2', arriveTime=0, needtime=3, pri=1))
        while not rr.run_one_step():
            processes = rr.get_all_process()
            print(processes)
        processes = rr.get_all_process()
        print(processes)