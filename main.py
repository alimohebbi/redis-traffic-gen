from concurrent.futures import ThreadPoolExecutor

import generator

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(generator.controller)
        executor.submit(generator.executor)

