from config import Config
from executor import Executor

if __name__ == "__main__":
    executor = Executor(Config())
    executor.start()
