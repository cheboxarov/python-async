def gen1(n):
    for i in n:
        yield i


def gen2(n):
    for i in range(n):
        yield i+1


g1 = gen1("иванева")
g2 = gen2(4)

tasks = [g1, g2]

while tasks.__len__() > 0:
    task = tasks.pop()
    try:
        i = next(task)
        print(i)
        tasks.insert(0, task)
    except StopIteration:
        pass
