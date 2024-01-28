import os, logging
from datetime import datetime

DEBUG = True

ACCESS_KEY = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
SECRET_KEY = os.environ['UPBIT_OPEN_API_SECRET_KEY']
SERVER_URL= os.environ['UPBIT_OPEN_API_SERVER_URL']

# Configure the logging settings
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join("output", f"{datetime.now().strftime('%m%d')}-{datetime.now().time().strftime('%H%M%S')}.txt"),  # Log file name
    filemode='w'  # Log file mode ('w' for write, 'a' for append)
)

# Create a logger object
logger = logging.getLogger('my_logger')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the desired logging level
logger.addHandler(console_handler)