from src.start_bot import start_bot
from src.utils import setup_logger
from src.utils import schedule_func



if __name__ == '__main__':
    setup_logger()
    start_bot()
    schedule_func()