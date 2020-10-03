import asyncio
from asyncio import wait_for, wrap_future, get_event_loop
from concurrent import futures
from time import sleep

def crunch(msg, times, interval=1):
    for i in range(times):
        print(msg)
        sleep(interval)

def blocking_io():
    print('Start blocking')
    crunch('Blocking in progress', 10, 2)
    print('Blocking done')

    return

async def ablocking_io():
    print('Start blocking synchornously')
    crunch('Blocking in sync', 10, 2)
    print('Sync blocking done')

async def small_task():
    print('Doing something small')
    value = 'small thing done'
    crunch('Just something small', 5)
    # our big task is probably awake now but still waiting for this small task to be done
    print('small thing is not done yet, keep working')
    sleep(1)
    print('small task is done, exiting')

    return value

async def big_task(executor):
    print('Doing something big')
    sleep(2)
    print('Still doing it')
    sleep(2)
    print('About to take a break')

    # asyncio.sleep() will suspend this task and wake up after 5 seconds
    # we want to substitute this with an io blocking task.
    # when this big task is waiting for io blocking, we want to switch to another task
    # instead of keep waiting here.
    # but the current task, i.e. the big_task needs to stop and wait

    # await asyncio.sleep(5)
    # print('Back to work')

    # loop = get_event_loop()

    # # blocking_tasks = [
    # #         loop.run_in_executor(executor, blocking_io)
    # # ]
    # # completed, pending = await asyncio.wait(blocking_tasks)
    # # results = [t.result() for t in completed]
    # # print('Results are:', results)

    # result = await loop.run_in_executor(executor, blocking_io)

    await ablocking_io()
    sleep(2)
    print('Big task is also done')


def main():
    executor = futures.ProcessPoolExecutor(max_workers=3)
    loop = get_event_loop()
    loop.create_task(big_task(executor))
    loop.create_task(small_task())

    loop.run_forever()

async def main2():
    executor = futures.ProcessPoolExecutor(max_workers=3)
    loop = get_event_loop()
    tasks = [
        loop.run_in_executor(executor, big_task(executor)),
        loop.run_in_executor(executor, small_task())
    ]

    await asyncio.wait(tasks)

if __name__ == '__main__':
    main()
