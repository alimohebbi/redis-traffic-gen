import datetime

from concurrent.futures import ThreadPoolExecutor

import generator

if __name__ == "__main__":
    generator.Stats.start_time = datetime.datetime.now()
    with ThreadPoolExecutor() as executor:
        f1 = executor.submit(generator.controller)
        f2 = executor.submit(generator.executor)
        f1.result()
        f2.result()
