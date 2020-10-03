def simple_generator():
    name_list = ['Bob', 'Anthony', 'Cyle', 'Dylan']

    for name in name_list:
        print('Current name is:', name)
        yield name
        print('simple_generator is resumed')

    print('######################')
    print('Generator is out of value')
    print('######################')


if __name__ == '__main__':
    gen = simple_generator()
    print(gen)

    for rec in gen:
        print('Value of gen:', rec)
        print('About to fecth next record from generator')


    another_gen = simple_generator()

    print('First element of another_gen:', next(another_gen))
    print('Second element of another_gen:', next(another_gen))
    print('Third element of another_gen:', next(another_gen))
    print('Fourth element of another_gen:', another_gen.__next__())
    try:
        print('Fifth element of another_gen:', next(another_gen))
    except StopIteration:
        print('No more value from generator')
