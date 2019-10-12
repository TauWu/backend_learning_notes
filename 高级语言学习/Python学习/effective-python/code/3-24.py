# -*- coding: utf-8 -*-

# Not use classmethod
import os
from threading import Thread


def safeopen(path):
    try:
        data = open(path).read()

    except IsADirectoryError:
        print("is a dir =>", path)
        return ""

    except Exception as e:
        print("read failed, err:", e)
        return ""

    else:
        return data

class InputData(object):

    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return safeopen(self.path)

class Worker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError

class LineCountWorker(Worker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other):
        self.result += other.result

def generate_inputs(data_dir):
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))

def create_workers(input_list):
    workers = []
    for input_data in input_list:
        workers.append(LineCountWorker(input_data))
    return workers

def execute(workers):
    threads = [Thread(target=w.map) for w in workers]
    for t in threads: t.start()
    for t in threads: t.join()

    first, rest = workers[0], workers[1:]
    for worker in rest:
        first.reduce(worker)

    return first.result

def mapreduce(data_dir):
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)
    return execute(workers)

result = mapreduce("../")
print(result)

# Use classmethod
class GenericInputData(object):

    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError

class PathInputData1(GenericInputData):

    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return safeopen(self.path)

    @classmethod
    def generate_inputs(cls, config):
        data_dir = config['data_dir']
        for name in os.listdir(data_dir):
            yield cls(os.path.join(data_dir, name))

class GenericWorker(object):

    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

class LineCountWorker1(GenericWorker):

    def map(self):
        data = self.input_data.read()
        self.result = data.count("\n")

    def reduce(self, other):
        self.result += other.result

    
def mapreduce1(worker_class, input_class, config):
    workers = worker_class.create_workers(input_class, config)
    return execute(workers)

result = mapreduce1(LineCountWorker1, PathInputData1 ,{"data_dir": "../"})
print(result)
