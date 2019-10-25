import logging
import concurrent.futures as cf
from itertools import repeat
from time import sleep
from bash_executor import cmd_executor
from config import Config

log_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")
config = Config()


def request_thread(name, step):
    logging.info("Thread %s of step %s", name, step)
    file_path = config.log_path + "/step-%s.txt" % step
    f = open(file_path, "a+")
    byte_out, byte_err = cmd_executor()
    str_out = byte_out.decode("utf-8")
    err_out = byte_err.decode("utf-8")
    out = "***Thread %a Begin***\n" % name + str_out + err_out + "***Thread %a End***\n" % name
    f.write(out)
    f.close()

    # if byte_err is not None:
    #     logging.error(byte_err.decode("utf-8"))

    logging.info("Done thread %s of step %s", name, step)


def generate():
    for step, load in enumerate(config.profile):
        with cf.ThreadPoolExecutor(max_workers=load) as executor:
            executor.map(request_thread, range(load), repeat(step))
