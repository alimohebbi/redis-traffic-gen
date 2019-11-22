import datetime
from threading import Thread

from bash_executor import cmd_executor
from report import write_memtier_report


def request_thread(name, start_time, process):
    byte_out, byte_err = process().communicate()
    write_memtier_report(byte_out, byte_err, name, start_time)


class TrafficGeneratorThread(Thread):
    _start_time = None
    _process = None

    def __init__(self, name, start_time):
        args = (name, start_time, self.get_process,)
        super(TrafficGeneratorThread, self).__init__(target=request_thread, args=args)

    def get_process(self):
        return self._process

    def get_age(self):
        age = (datetime.datetime.now() - self._start_time).total_seconds()
        return int(age)

    def stop(self):
        try:
            self._process.kill()
        except Exception as e:
            print e

    def start(self):
        self._start_time = datetime.datetime.now()
        self._process = cmd_executor(None)
        super(TrafficGeneratorThread, self).start()
        # print "Thread started"
