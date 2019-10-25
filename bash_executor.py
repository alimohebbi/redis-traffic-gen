import random
import subprocess

from config import Config

config = Config()


def create_command():
    bm = config.benchmark
    server = random.choice(config.servers)
    cmd = f"memtier_benchmark -s {server} -p {bm.port} -c {bm.clients} -t {bm.threads} -d {bm.data_volume} " \
        f"--ratio={bm.data_volume} --pipeline=1 --key-pattern S:S --cluster-mode -P redis " \
        f"--test-time={config.time_steps}"

    return cmd


def cmd_executor(command=create_command()):
    pip_open = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    return pip_open.communicate()


if __name__ == "__main__":
    out, err = cmd_executor()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))
