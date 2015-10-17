__title__ = 'aptparser'
__version__ = '0.0.0'
__build__ = 0x000000
__author__ = 'luming hao'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 luming hao'
# i don't even know what this stuff means



from .api import search, read
from .parser import parse_id, parse_description, parse_price, parse_neighborhood, parse_title, parse_address, parse_time_to_work
from .googlemaps import get_travel_time


# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):

        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
