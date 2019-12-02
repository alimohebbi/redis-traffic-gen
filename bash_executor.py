import random
import socket
import subprocess

from config import Config

config = Config()


def check_server(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #    sock.settimeout(10)
    result = sock.connect_ex((server, config.benchmark.port))
    if result == 0:
        return True
    return False


def get_command_args():
    bm = config.benchmark
    server = select_server()
    args = (server, bm.port, bm.clients, bm.threads, bm.data_volume, bm.ratio, config.time_steps, bm.expiry_range)
    return args


def create_command(prefix):

    args = get_command_args()
    args = args + (prefix,)
    cmd = "memtier_benchmark -s {} -p {} -c {} -t {} -d {} --ratio={} --pipeline=1 --key-pattern S:S --cluster-mode " \
          "-P redis --test-time={} --expiry-range={} --key-prefix={}".format(*args)

    return cmd


def select_server():
    server = None
    server = random.choice(config.servers)

    # for i in range(config.connection_retry):
    #     candid_server = random.choice(config.servers)
    #     if check_server(candid_server):
    #         server = candid_server
    #         break
    # if server is None:
    #     raise RuntimeError("None of servers are available")
    return server


def cmd_executor(prefix):
    command = create_command(prefix)
    pip_open = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    return pip_open


if __name__ == "__main__":
    out, err = cmd_executor()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))
