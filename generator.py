import datetime
import logging
from itertools import repeat
from time import sleep

import concurrent.futures as cf
from tqdm import tqdm

from bash_executor import cmd_executor
from config import Config
from report import write_report

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
config = Config()


def request_thread(name, start_time):
    byte_out, byte_err = cmd_executor()
    write_report(byte_out, byte_err, name, start_time)


def generate():
    start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for load in tqdm(config.profile, desc='Test Progress'):
        with cf.ThreadPoolExecutor(max_workers=load) as executor:
            # executor.map(request_thread, range(load), repeat(start_time))
            for i in tqdm(range(load), desc='Step progress'):
                executor.submit(request_thread, i, start_time)
                sleep(1)
