from queue import Queue
from task import Task, my_coroutine
from syscall import GetTaskID, SystemCall


class Scheduler:

    def __init__(self):
        self.ready = Queue()
        self.task_map = {}

    def new(self, target):
        task = Task(target)
        self.task_map[task.tid] = task
        self.schedule(task)
        return task.tid

    def schedule(self, task):
        self.ready.put(task)

    def exit(self, task):
        print('Removing task #', task.tid,'from task_map')
        del(self.task_map[task.tid])

    def mainloop(self):
        print('Main program starts')
        while self.task_map:
            print('Reading task')
            task = self.ready.get()
            if task:
                try:
                    print('running task #', task.tid)
                    result = task.run()
                    print('result from task running', result)
                    if isinstance(result, SystemCall):
                        print('Triggering a system call')
                        result.task = task
                        result.sched = self
                        result.handle()
                except StopIteration:
                    print('task #', task.tid,'is done')
                    self.exit(task)
                    continue

                print('main thread resumes with result:', result)

            print('Re-schedule task #', task.tid)
            self.schedule(task)

        print('task_map is empty now, existing program')


def routine_with_syscall():
    my_id = yield GetTaskID()
    for i in range(5):
        print('routine_with_syscall has id:', my_id)


if __name__ == '__main__':
    sched = Scheduler()
    sched.new(routine_with_syscall())
    sched.mainloop()
