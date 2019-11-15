import datetime
import os
import re
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
    f = open(file_path, "a+")
    if not os.path.exists(file_path):
        if path == config.log_path:
            f.write("Timestamps,Thread,Ops/sec,Hits/sec,Misses/sec,MOVED/sec,ASK/sec,Latency,KB/sec\n")
        else:
            f.write("Timestamps,Thread,Ops\n")
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


def write_report(byte_text, byte_error, name, start_time):
    setup_dir()
    write_log(byte_text, config.log_path, name, start_time)
    write_log(byte_error, config.error_path, name, start_time)
    write_csv(byte_text, config.log_path, name, start_time)
    write_csv(byte_error, config.error_path, name, start_time)


if __name__ == '__main__':
    f = open("logs/log-sample.txt", "r")
    content = f.read()
    print get_measures_from_error(content)
