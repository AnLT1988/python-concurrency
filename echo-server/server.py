import asyncio
from asyncio import get_event_loop, wait, wait_for
from collections import namedtuple

People = namedtuple('People', ['name', 'delay'])


class EchoServer:

    def __init__(self):
        print('Server has initialized')

    def run(self):
        print('Server is started and running')
        # loop.run_until_complete(self.main())
        asyncio.run(self.main())
        # pendings = asyncio.all_tasks(loop)
        # print('Pending tasks:', pendings)
        # loop.run_until_complete(asyncio.gather(*pendings))


    async def main(self):
        tasks = []
        people = [
            People('Annie', 2),
            People('Bella', 1),
            People('Ciri', 5),
            People('Duke', 10),
        ]
        for person in people:
            loop = asyncio.get_running_loop()
            print(loop)
            tasks.append(asyncio.create_task(self.greeting(person.name, person.delay)))
            print(person.name, 'task created')
            print('main going to sleep')
            await asyncio.sleep(1)
            print(f'################## MAIN ####################')

        print('pending tasks:', tasks)
        await asyncio.gather(*tasks)

        print('Existing main')

    async def greeting(self, name, delay=0):
        print(f'################## {name} Task Started ####################')
        print('Hello there', name)
        await self.task_switch(delay)
        print('task resume')
        print('Hello again', name)
        print(f'################## {name} Task Stopped ####################')


    async def task_switch(self, delay):
        print('task sleep for', delay)
        await asyncio.sleep(delay)



if __name__ == '__main__':
    server = EchoServer()
    server.run()
