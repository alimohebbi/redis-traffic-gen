import subprocess

from config import Config

config = Config()

def create_command():
    cmd = list()
    cmd.append("memtier_benchmark")
    cmd.append("-s 192.168.200.165 -p 6378 -c 3 -t 2 -d 1024 --ratio=1:1 "
               "--pipeline=1 --key-pattern S:S --cluster-mode -P redis --test-time=%s" % config.time_steps)
    return cmd


def cmd_executor(command=create_command()):
    pip_open = subprocess.Popen(command,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    return pip_open.communicate()
