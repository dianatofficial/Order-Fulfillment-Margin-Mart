import logging
import sys
from rich.logging import RichHandler

def setup_logger(name: str = 'order_mart') -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        rich_handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=True,
            show_path=False
        )
        formatter = logging.Formatter('%(message)s')
        rich_handler.setFormatter(formatter)
        logger.addHandler(rich_handler)
    return logger

logger = setup_logger()
