from entity.process import Process
from abc import ABC, abstractmethod
class Schedule(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def get_next_process(self):
        pass
    @abstractmethod
    def run_one_step(self):
        pass
    @abstractmethod
    def wakeup(self, process):
        pass
    @abstractmethod
    def stop(self,process):
        pass
    @abstractmethod
    def add_process(self, process):
        pass
    @abstractmethod
    def remove_process(self, process):
        pass
    @abstractmethod
    def check_finish(self):
        pass

    @abstractmethod
    def get_all_process(self):
        pass

