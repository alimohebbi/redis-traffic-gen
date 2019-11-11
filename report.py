import datetime
import os
import re


def get_measures(text):
    begin = text.find("Totals")
    end = text.find('\n', begin)
    sub = text[begin + 'Totals'.__len__():end]
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


def csv_file(path, start_time):
    file_path = path + "/%s.csv" % start_time

    if not os.path.exists(file_path):
        f = open(file_path, "a+")
        f.write("Timestamps,Thread,Ops/sec,Hits/sec,Misses/sec,MOVED/sec,ASK/sec,Latency,KB/sec")
    else:
        f = open(file_path, "a+")
    return f


def write_csv(byte_text, path, name, start_time):
    f = csv_file(path, start_time)
    str_text = byte_text.decode("utf-8")
    measures = get_measures(str_text)
    current_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    out = "%s,%s\n" % (current_time, name) + measures
    f.write(out)
    f.close()


def write_report(byte_text, path, name, start_time):
    if not os.path.exists(path):
        os.makedirs(path)
    write_log(byte_text, path, name, start_time)
    write_csv(byte_text, path, name, start_time)


if __name__ == '__main__':
    f = open("log-sample.txt", "r")
    content = f.read()
    print get_measures(content)
