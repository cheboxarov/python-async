from inspect import getgeneratorstate


def coroutine(func):
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return wrapper


def subgen():
    x = "Ready to accept message"
    message = yield x
    message2 = yield
    print("Subgen received", message, message2)


def test_subgen():
    g = subgen()
    print(getgeneratorstate(g))
    print(g.send(None))
    print(getgeneratorstate(g))
    try:
        g.send("123")
        g.send("123123123")
    except StopIteration:
        pass


@coroutine
def get_average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print("Done")
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
    return average


def test_average():
    gen = get_average()
    print(gen.send(1))
    print(gen.send(2))
    print(gen.send(34553))
    try:
        gen.throw(StopIteration)
    except StopIteration as average:
        print(f"Final average: {average.value}")


if __name__ == "__main__":
    test_average()
