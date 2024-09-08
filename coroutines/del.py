def coroutine(func):
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return wrapper


class MyException(Exception):
    pass


def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            print("kuku")
            break
        else:
            print(f"------- {message}")
    return "Returned from subgen()"


@coroutine
def delegator(g):
    result = yield from g
    return result


def test_delegator():
    sg = subgen()
    g = delegator(sg)
    g.send("asd")
    g.send("asd")
    g.send("asd")
    try:
        g.throw(StopIteration)
    except StopIteration as result:
        print(result.value)


if __name__ == '__main__':
    test_delegator()