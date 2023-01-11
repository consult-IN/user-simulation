import logging
from dotenv import load_dotenv

# make sure the .env is available in your root directory
load_dotenv()
LOG_LEVEL = logging.DEBUG

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")


logger = logging.getLogger("user_sim_logger")
logger.setLevel(LOG_LEVEL)

consoleHandler = logging.StreamHandler()

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(LOG_LEVEL)
