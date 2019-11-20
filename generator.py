import datetime
import logging
from Queue import Queue
from threading import Thread
from time import sleep
import concurrent.futures as cf
from tqdm import tqdm
from bash_executor import cmd_executor
from config import Config
from report import write_report

config = Config()
new_thread_q = Queue()
thead_list = list()


def request_thread(name, start_time, process):
    byte_out, byte_err = process().communicate()
    write_report(byte_out, byte_err, name, start_time)


def generate():
    start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for load in tqdm(config.profile, desc='Test Progress'):
        with cf.ThreadPoolExecutor(max_workers=load) as executor:
            # executor.map(request_thread, range(load), repeat(start_time))
            for i in tqdm(range(load), desc='Step progress'):
                executor.submit(request_thread, i, start_time)
                sleep(1)


class TrafficGeneratorThread(Thread):
    _start_time = None
    _process = None

    def __init__(self, target, args):
        args = args + (self.get_process,)
        super(TrafficGeneratorThread, self).__init__(target=target, args=args)

    def get_process(self):
        return self._process

    def get_age(self):
        return datetime.datetime.now() - self._start_time

    def stop(self):
        self._process.kill()

    def start(self):
        self._start_time = datetime.datetime.now()
        self._process = cmd_executor()
        super(TrafficGeneratorThread, self).start()
        print "start end"


def kill_locked_thread():
    for tg_thread in thead_list:
        if tg_thread.get_age() > config.time_steps * config.thread_life_limit:
            pass


def calculate_new_threads_num():
    pass


def add_new_threads_to_q():
    pass


def controller():
    limit = config.profile.__len__() * config.time_steps
    start_time = datetime.datetime.now()
    controller_age = 0
    while thead_list.count() == 0 or controller_age < limit:
        controller_age = datetime.datetime.now() - start_time
        kill_locked_thread()
        calculate_new_threads_num()
        add_new_threads_to_q()


def executor():
    pass


if __name__ == "__main__":
    ex = cf.ProcessPoolExecutor(max_workers=3)
    f = TrafficGeneratorThread(request_thread, ("heh", datetime.datetime.now()))
    f.start()
    print "here"
    sleep(15)
    print "here"
    f.stop()
    print "here"
