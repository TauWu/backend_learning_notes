#!usr/bin/python
# -*- coding:utf-8 -*-

def gen(size):
    for i in range(0, size):
        yield i

if __name__ == "__main__":
    generator = gen(5)
    for x in generator:
        print(x)

    generator = gen(5)
    while True:
        try:
            print(next(generator))
        except Exception:
            break
