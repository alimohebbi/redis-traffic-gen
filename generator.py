import datetime
import logging
from Queue import Queue
from time import sleep

from config import Config
from report import write_stats
from traffic_thread import TrafficGeneratorThread

config = Config()
new_thread_q = Queue()
thead_list = list()
execution_start_time = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)


def executor():
    while execution_has_time() and Stats.status == 'OK':
        if not new_thread_q.empty():
            thread = new_thread_q.get()
            thread.start()
            thead_list.append(thread)
        sleep(config.controller.execute_frequency)
    logging.debug("executor finished")


def controller():
    Stats.total_iterations = config.time_steps * config.profile.__len__() / config.controller.control_frequency
    while thead_list.__len__() != 0 or execution_has_time():
        try:
            kill_locked_thread()
            new_thread_num, step = calculate_new_threads_num()
            add_new_threads_to_q(new_thread_num, step)
            write_stats(Stats)
        except Exception as e:
            write_stats(Stats)
            logging.error(e)
            write_stats(Stats)
            break

        Stats.iterations += 1
        sleep(config.controller.control_frequency)


def add_new_threads_to_q(num, step):
    for i in range(num):
        start_time = execution_start_time.strftime('%Y-%m-%dT%H:%M:%S')
        thread = TrafficGeneratorThread(step, start_time)
        new_thread_q.put(thread)


def calculate_new_threads_num():
    current_time = datetime.datetime.now()
    time_elapsed = (current_time - execution_start_time).total_seconds()
    profile_index = int(time_elapsed / config.time_steps)
    if config.profile.__len__() <= profile_index:
        Stats.new_threads = 0
        return 0, 0
    required_num = config.profile[profile_index]
    new_num = required_num - thead_list.__len__() - new_thread_q.qsize()
    Stats.new_threads = new_num
    return new_num, profile_index


def kill_locked_thread():
    kill_count = 0
    finish_count = 0
    early_finish = 0
    for tg_thread in thead_list:
        if tg_thread.get_age() > config.time_steps * config.controller.thread_life_limit:
            tg_thread.stop()
            thead_list.remove(tg_thread)
            kill_count += 1
        elif not tg_thread.is_alive():
            thead_list.remove(tg_thread)
            if tg_thread.get_age() < config.time_steps:
                early_finish += 1
            else:
                finish_count += 1
    check_health(early_finish, finish_count, kill_count)


def check_health(early_finish, finish_count, kill_count):
    set_threads_stats(kill_count, finish_count, early_finish)
    if kill_count > config.controller.stop_tolerance:
        Stats.status = 'Fail'
        raise Exception("Too many threads not responding")
    if early_finish > config.controller.early_finish_tolerance:
        Stats.status = 'Fail'
        raise Exception("Too many thread finished early")


def execution_has_time():
    limit = config.profile.__len__() * config.time_steps
    controller_age = (datetime.datetime.now() - execution_start_time).total_seconds()
    return controller_age < limit


class Stats:
    new_threads = 0
    in_queue = 0
    killed = 0
    finished = 0
    early_finish = 0
    status = 'OK'
    total_iterations = 0
    iterations = 0
    active_threads = 0
    start_time = None

    def __init__(self):
        pass


def set_threads_stats(kill_count, finish_count, early_finish):
    Stats.killed += kill_count
    Stats.finished += finish_count
    Stats.early_finish += early_finish
    Stats.active_threads = thead_list.__len__()
    Stats.in_queue = new_thread_q.qsize()


if __name__ == "__main__":
    f = TrafficGeneratorThread('1', "MY-Test-Result")
    sleep(2)
    f.start()
    logging.debug("after start")
    sleep(2)
    print f.is_alive()
    sleep(60)
    print f.is_alive()
