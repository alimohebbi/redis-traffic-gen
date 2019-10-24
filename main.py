import generator
from config import Config
from bash_executor import cmd_executor

if __name__ == "__main__":
    args = ((a, 2) for a in range(4))
    print(list(args))
    generator.generate()



