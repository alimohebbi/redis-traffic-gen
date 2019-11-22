import curses
import datetime
import os
import re
import sys
from time import sleep

from config import Config

config = Config()


def get_measures_from_log(text):
    begin = text.find("Totals")
    end = text.find('\n', begin)
    sub = text[begin + 'Totals'.__len__():end]
    sub = sub.strip()
    sub = re.sub(' +', ',', sub)
    return sub


def get_measures_from_error(text):
    begin = text.find("threads:")
    end = text.find('ops', begin)
    sub = text[begin + 'threads:'.__len__():end]
    sub = sub.strip()
    sub = re.sub(' +', ',', sub)
    return sub


def write_log(byte_text, path, name, start_time):
    file_path = path + "/%s.txt" % start_time
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    f = open(file_path, "a+")
    str_text = byte_text.decode("utf-8")
    out = "%s ***Thread %s Begin***\n" % (current_time, name) + str_text + "***Thread %s End***\n" % name
    f.write(out)
    f.close()


def create_csv_file(path, start_time):
    file_path = path + "/%s.csv" % start_time
    if not os.path.exists(file_path):
        f = open(file_path, "a+")
        if path == config.log_path:
            f.write("Timestamps,Thread,Ops/sec,Hits/sec,Misses/sec,MOVED/sec,ASK/sec,Latency,KB/sec\n")
        else:
            f.write("Timestamps,Thread,Ops\n")
    else:
        f = open(file_path, "a+")
    return f


def get_measures(str_text, path):
    if path == config.log_path:
        return get_measures_from_log(str_text)
    else:
        return get_measures_from_error(str_text)


def write_csv(byte_text, path, name, start_time):
    f = create_csv_file(path, start_time)
    str_text = byte_text.decode("utf-8")
    measures = get_measures(str_text, path)
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    out = "%s,%s," % (current_time, name) + measures + '\n'
    f.write(out)
    f.close()


def setup_dir():
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)
    if not os.path.exists(config.error_path):
        os.makedirs(config.error_path)


def write_memtier_report(byte_text, byte_error, name, start_time):
    setup_dir()
    write_log(byte_text, config.log_path, name, start_time)
    write_log(byte_error, config.error_path, name, start_time)
    write_csv(byte_text, config.log_path, name, start_time)
    write_csv(byte_error, config.error_path, name, start_time)


def write_stats(stats):
    measures = stats.status, stats.active_threads, stats.finished, stats.killed, stats.new_threads, stats.early_finish
    measures += (stats.in_queue,)
    progress = int(stats.iterations / float(stats.total_iterations) * 100)
    time_dic = {}
    controller_age = datetime.datetime.now() - stats.start_time
    time_dic['elapsed'] = str(controller_age).split(".")[0]
    time_dic['iterations'] = stats.iterations
    if stats.iterations == 0:
        time_dic['avg_it'] = 0
    else:
        time_dic['avg_it'] = str(controller_age.total_seconds() / stats.iterations).split(".")[0]
    seconds_remain = int(time_dic['avg_it']) * (stats.total_iterations - stats.iterations)
    time_dic['remain'] = datetime.timedelta(seconds=seconds_remain)
    update_progress(progress, measures, time_dic)


if __name__ == "__main__":
    for i in range(100):
        sleep(1)
        sys.stdout.write("\r%d%%" % i)
        sys.stdout.flush()


def update_progress(progress, desc, time_dic):
    stdscr = curses.initscr()
    t = (time_dic['elapsed'], time_dic['iterations'], time_dic['avg_it'], time_dic['remain'])
    titles = 'Status | Active | Finished | Killed | New | Early Finished | In Queue'
    stdscr.addstr(0, 0, "Measure: {0}".format(titles))
    stdscr.addstr(1, 0, "Stats  : {:<8} {:<8} {:<10} {:<8} {:<6} {:<15} {:<10}".format(*desc))
    stdscr.addstr(3, 0, "Total progress: [{1:50}] {0}%".format(progress, "#" * (progress / 2)))
    stdscr.addstr(4, 0, "Time Elapsed: %s     Iteration: %s     Iteration/s: %s     Remain: %s" % t)
    stdscr.refresh()
