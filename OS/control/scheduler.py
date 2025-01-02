# 用来负责调控使用什么算法
from entity.process import Process
from schedule.cfs import CFS
from schedule.rr import RR
from schedule.fcfs import FCFS

class Scheduler:

    T = 0

    def __init__(self, val=None, time_part = None):
        if val is None:
            pass
        elif val == 'FCFS':
            self.sche = FCFS()
        elif val == 'RR':
            self.sche = RR()
            if time_part is not None:
                self.sche.time_part = time_part
        else:
            self.sche = CFS()


    def add_process(self, pro):
        # pro = Process(PID, arriveTime, needTime, priority)
        self.sche.add_process(pro)
    def remove_process(self, PID):
        self.sche.remove_process(PID)
    def run_one_step(self)->bool: # 运行结束返回True， 否则False
        f = self.sche.run_one_step()
        self.T = self.sche.T
        return f
    def wakeup(self, PID):
        self.sche.wakeup(PID)
    def stop(self, PID):
        self.sche.stop(PID)
    def get_all_processes(self):
        return self.sche.get_all_process()



