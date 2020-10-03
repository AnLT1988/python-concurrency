class SystemCall:
    pass

class GetTaskID(SystemCall):

    def __init__(self):
        print('Get task id')

    def handle(self):
        self.task.send_val = self.task.tid
        self.sched.schedule(self.task)
