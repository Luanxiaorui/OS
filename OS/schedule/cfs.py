from typing import List

from entity.process import Process
from entity.sche import Schedule
import heapq


class CFS(Schedule):

    nices = [ 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    weight = 32
    readyQue = []  # 就绪队列
    not_arrive = [] # 未到达的队列
    blockList = []  # 阻塞队列
    finishedList = []  # 完成队列
    T = 0  # 总时间
    time_part = 1  # 时间片，默认为1

    def __init__(self):
        pass

    def cal_priority(self, pro)->int:
        val =   pro.runtime * self.weight / self.nices[(pro.nice % len(self.nices) + len(self.nices)) % len(self.nices) ]  # 进程优先级计算
        pro.priority = val
        return val

    def add_process(self, pro:Process):  # 加入一个进程
        if pro.arriveTime <= self.T:
            heapq.heappush(self.readyQue, (self.cal_priority(pro), pro))
        else:
            pro.state = 'waiting'
            self.not_arrive.append(pro)

    def remove_process(self, PID):  # 移除一个进程
        for queue in [self.not_arrive, self.blockList]:
            pro = next((p for p in queue if p.pid == PID), None)
            if pro:
                queue.remove(pro)
                break
        for item in self.readyQue:
            if item[1].pid == PID:
                self.readyQue.remove(item)
                break


    def get_next_process(self):# 获得这一时刻要运行的进程

        # 将到时间的全部放进就绪队列
        for pro in self.not_arrive:
            if pro.arriveTime <= self.T:
                pro.state = 'READY'
                heapq.heappush(self.readyQue, (self.cal_priority(pro), pro))
                self.not_arrive.remove(pro)

        # 从就绪队列中找到优先级最高的
        if self.readyQue:
            priority, pro = heapq.heappop(self.readyQue)
            pro.state = 'RUNNING'
            return pro
        return None

    def run_one_step(self) ->bool:  # 每次运行一个时间片, 运行结束返回True， 否则False
        pro:Process = self.get_next_process()

        if pro is not None:
            if pro.startTime == -1:
                pro.startTime = self.T
            pro.runtime += self.time_part
            pro.needTime -= self.time_part
            if pro.needTime > 0:
                pro.state = 'READY'
                heapq.heappush(self.readyQue, (self.cal_priority(pro), pro))
            else:
                pro.endTime = self.T + self.time_part
                pro.state = 'FINISH'
                self.finishedList.append(pro)
        self.T += self.time_part

        pro = self.get_next_process()
        if pro is not None:
            pro.state = 'RUNNING'
            heapq.heappush(self.readyQue, (self.cal_priority(pro), pro))
        return self.check_finish()

    def wakeup(self, PID):  # 唤醒进程
        for pro in self.blockList:
            if pro.pid == PID:
                pro.state = 'READY'
                heapq.heappush(self.readyQue, (self.cal_priority(pro), pro))
                self.blockList.remove(pro)
                break

    def stop(self, PID):  # 阻塞进程
        for (priority, pro) in self.readyQue:
            if pro.pid == PID:
                pro.state = 'BLOCK'
                self.blockList.append(pro)
                self.readyQue.remove((priority, pro))
                break

    def check_finish(self):
        return len(self.readyQue) == 0 and len(self.not_arrive) == 0 and len(self.blockList) == 0

    def get_all_process(self)->List[Process]:
        all_processes = self.not_arrive + [item[1] for item in self.readyQue] + self.blockList + self.finishedList
        return all_processes


# if __name__ == '__main__':
#     cfs = CFS()
#     cfs.add_process(Process('1', 2, 3, 0))
#     cfs.add_process(Process('2', 2, 3, 1))
#     while not cfs.run_one_step():
#         print(cfs.get_all_process())
#     print(cfs.get_all_process())



