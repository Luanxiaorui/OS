class Process:

    pid = '***'
    Pname = '***'
    arriveTime = 0 # 到达时间
    startTime = -1 # 实际开始的运行时间
    runtime = 0 # 已经运行的时间
    needTime = 0 # 剩余所需时间
    endTime = 0 # 运行结束时间
    state = 'WAIT' # 进程状态
    wakeTime = 0 # 阻塞之后，唤醒时间
    priority = 0 # 默认优先级
    nice = 0 # 默认序列号

    def __init__(self, PID = None, Pname = None, arriveTime = None, needtime =None, pri=None):
        if PID is not None:
            self.pid = PID
        if arriveTime is not None:
            self.arriveTime = arriveTime
        if needtime is not None:
            self.needTime = needtime
        if pri is not None:
            self.nice = pri
        if Pname is not None:
            self.Pname = Pname

    def __str__(self):
        return f"Process(PID={self.pid}, arrivetime={self.arriveTime}, needtime={self.needTime})"
    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.priority < other.priority  # 根据进程的 pid 比较


    def getArriveTime(self):
        return self.arriveTime
    def getRuntime(self):
        return self.runtime
    def getNeedTime(self):
        return self.needTime
    def getStatus(self):
        return self.status
    def getPID(self):
        return self.PID
    def getEndTime(self):
        return self.endTime

    def setneedTime(self, needTime):
        self.needTime = needTime
    def setruntime(self, runtime):
        self.runtime = runtime
    def setStatus(self, status):
        self.state = status
    def setEndTime(self, endTime):
        self.endTime = endTime


