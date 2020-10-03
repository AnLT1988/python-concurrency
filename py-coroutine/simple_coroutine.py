def simple_coroutine():
    print('Coroutine starts')
    keep_running = True
    while keep_running:
        # Notice that yield is used as an expression
        # which will suspend the current process of simple_coroutine
        # to give control to whoever call next() on simple_coroutine
        # but also assigns value from next simple_coroutine.send(value)
        # to variable _input and continues the process of simple_coroutine
        _input = yield
        print('Coroutine resumes')
        print('Input from outside:', _input)
        if _input == "quit":
            keep_running = False

    print('Coroutine stops')


if __name__ == '__main__':
    routine = simple_coroutine()
    print(routine)

    # This is to start the coroutine
    routine.__next__()

    try:
        input_value = ['First input', 'Second input', 'quit']
        for _input in input_value:
            print('About to send input to coroutine')
            routine.send(_input)
            print('Looking for next input to feed the coroutine')
    except StopIteration:
        print('Coroutine has stopped')

    print('Exiting...')


