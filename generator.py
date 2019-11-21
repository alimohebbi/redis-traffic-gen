import datetime
import logging
from Queue import Queue
from time import sleep

from tqdm import tqdm

from config import Config
from traffic_thread import TrafficGeneratorThread

config = Config()
new_thread_q = Queue()
thead_list = list()
execution_start_time = datetime.datetime.now()
logging.basicConfig(level=logging.DEBUG)


def executor():
    while execution_has_time():
        if not new_thread_q.empty():
            thread = new_thread_q.get()
            thread.start()
            thead_list.append(thread)
            # todo add to config
        logging.debug("executor")
        sleep(1)
    logging.debug("executor finished")


def controller():
    total = config.time_steps * config.profile.__len__() / 10
    pbar = tqdm(total=total)
    while thead_list.__len__() != 0 or execution_has_time():
        kill_locked_thread()
        new_thread_num, step = calculate_new_threads_num()
        add_new_threads_to_q(new_thread_num, step)
        # todo add to config
        logging.debug("controller create %s", new_thread_num)
        pbar.update()
        sleep(10)
    pbar.close()
    logging.debug("controller finished")


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
        return 0, 0
    required_num = config.profile[profile_index]
    return required_num - thead_list.__len__() - new_thread_q.qsize(), profile_index


def kill_locked_thread():
    count = 0
    for tg_thread in thead_list:
        if tg_thread.get_age() > config.time_steps * config.thread_life_limit:
            logging.debug("Thread Killed with age %s ", tg_thread.get_age())
            tg_thread.stop()
            thead_list.remove(tg_thread)
            count += 1
        if not tg_thread.is_alive():
            logging.debug("Thread Removed")
            thead_list.remove(tg_thread)

    # todo add to config
    if count > 20:
        raise Exception("Too many thread not responding")


def execution_has_time():
    limit = config.profile.__len__() * config.time_steps
    controller_age = (datetime.datetime.now() - execution_start_time).total_seconds()
    return controller_age < limit


if __name__ == "__main__":
    f = TrafficGeneratorThread(1, "MY-Test-Result")
    sleep(2)
    f.start()
    logging.debug("after start")
    sleep(2)
    print f.is_alive()
    sleep(60)
    print f.is_alive()
