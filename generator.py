from time import sleep

import concurrent.futures as cf
import logging
import os
from itertools import repeat
from tqdm import tqdm
from bash_executor import cmd_executor
from config import Config
import datetime

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
config = Config()


def request_thread(name, start_time):
    byte_out, byte_err = cmd_executor()
    write_log(byte_out, config.log_path, name, start_time)
    write_log(byte_err, config.error_path, name, start_time)


def write_log(byte_text, path, name, start_time):
    file_path = path + "/%s.txt" % start_time
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(file_path, "a+")
    err_out = byte_text.decode("utf-8")
    out = "%s ***Thread %s Begin***\n" % (current_time, name) + err_out + "***Thread %s End***\n" % name
    f.write(out)
    f.close()


def generate():
    start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    for load in tqdm(config.profile, desc='Test Progress'):
        with cf.ThreadPoolExecutor(max_workers=load) as executor:
            executor.map(request_thread, range(load), repeat(start_time))
        sleep(1)
