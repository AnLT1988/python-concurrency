from collections import deque
from concurrent.futures import Future
from asyncio import wait_for, wrap_future, get_event_loop
from threading import Thread
from time import sleep


class AQueue:

    def __init__(self, max_size):
        self.items = deque()
        self.max_size = max_size
        self.getters = deque()
        self.putters = deque()

    def get(self):
        if self.items:
            if self.putters:
                print('removing putters')
                self.putters.popleft().set_result(True)
            return self.items.popleft(), None
        else:
            fut = Future()
            self.getters.append(fut)
            return None, fut

    def put(self, item):
        if len(self.items) < self.max_size:
            self.items.append(item)
            if self.getters:
                self.getters.popleft().set_result(self.items.popleft())
        else:
            fut = Future()
            self.putters.append(fut)
            return fut

    def put_sync(self, item):
        while True:
            fut = self.put(item)
            if fut is None:
                print('Successfully put value', item, 'to queue')
                return
            print('Waiting in line to put value:', item, 'to queue')
            fut.result()
            print('Your time has come, put value', item, 'to queue')

    def get_sync(self):
        sleep(2)
        item, fut = self.get()
        if fut:
            item = fut.result()
        return item

    async def get_async(self):
        item, fut = self.get()
        if fut:
            item = await wait_for(wrap_future(fut), None)
        return item

    async def put_async(self, item):
        while True:
            fut = self.put(item)
            if fut is None:
                print('Successfully put value', item, 'to queue')
                return
            print('Waiting in line to put value:', item, 'to queue')
            await wait_for(wrap_future(fut), None)
            print('Your time has come, put value', item, 'to queue')


def consumer(q):
    while True:
        item = q.get_sync()
        if item is None:
            break
        print('Got:', item)

async def aproducer(q, n):
    for i in range(n):
        await q.put_async(i)
    await q.put_async(None)

if __name__ == '__main__':
    q = AQueue(2)

    loop = get_event_loop()
    Thread(target=lambda: (sleep(3), consumer(q))).start()
    loop.run_until_complete(aproducer(q, 10))
