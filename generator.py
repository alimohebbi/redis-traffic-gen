import concurrent.futures as cf
import logging
import os
from itertools import repeat

from bash_executor import cmd_executor
from config import Config

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
config = Config()


def request_thread(name, step):
    logging.info("Thread %s of step %s", name, step)

    byte_out, byte_err = cmd_executor()
    write_log(byte_err, byte_out, name, step)

    logging.info("Done thread %s of step %s", name, step)


def write_log(byte_err, byte_out, name, step):
    file_path = config.log_path + "/step-%s.txt" % step
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)
    f = open(file_path, "a+")
    str_out = byte_out.decode("utf-8")
    err_out = byte_err.decode("utf-8")
    out = "***Thread %a Begin***\n" % name + str_out + err_out + "***Thread %a End***\n" % name
    f.write(out)
    f.close()


def generate():
    for step, load in enumerate(config.profile):
        with cf.ThreadPoolExecutor(max_workers=load) as executor:
            executor.map(request_thread, range(load), repeat(step))
