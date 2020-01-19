import logging
from pythonjsonlogger import jsonlogger
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('miio')

format_str = '%(message)%(levelname)%(name)%(asctime)'

logHandler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(format_str)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
