"""The settings script is solely dedicated to parsing the application's
configuration files.
"""

import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


ADAPTERS = []
