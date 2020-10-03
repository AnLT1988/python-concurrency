class Task():

    task_id = 0

    def __init__(self, target):
        self.task_id += 1
        self.tid = self.task_id
        self.target = target
        self.send_val = None

    def run(self):
        return self.target.send(self.send_val)


def my_coroutine():
    print('Co routine starts')
    _input = yield
    print('Co routine continues')
    _input = yield
    print('Co routine stop')

if __name__ == '__main__':
    my_task = Task(my_coroutine())
    print("Run task first time")
    my_task.run()
    print("run task second time")
    my_task.run()
    print("run task third time")
    my_task.run()
