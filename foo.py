#!/usr/bin/env python

import asyncio
import signal
import pytest


class Foo:
    def __init__(self):
        self.request_to_stop = False

    async def start(self):
        self.request_to_stop = False

        count = 0
        while not self.request_to_stop:
            count += 1
            print(f"Foo: fooing task {count}...")
            await asyncio.sleep(1)

        print("Foo: Posso uscire graziosamente!")
        return count

    def stop(self):
        print("Foo: roger, but let me finish!")
        self.request_to_stop = True


@pytest.mark.asyncio
async def test_foo():
    foo = Foo()
    task = asyncio.Task(foo.start())
    await asyncio.sleep(0.5)
    foo.stop()
    await task
    assert foo.request_to_stop is True
    assert task.result() == 1

class GracefulKiller:
    def __init__(self, foo: Foo):
        self.foo = foo
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        print("GracefulKiller: telling Foo to stop...")
        self.foo.stop()


if __name__ == "__main__":
    foo = Foo()

    GracefulKiller(foo)

    print("Main: starting foo")
    asyncio.run(foo.start())
    print("Main: foo has ended!")
