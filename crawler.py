import logging
import traceback
import requests
import time

__author__ = "Deepak Patil"

from tabulate import tabulate
from time import sleep
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
log = logging.getLogger('__name__')

class crawler:

    def __init__(self, show_available, pincode, district):
        log.debug("__inside__")
        self.show = show_available
        self.pincode = pincode
        self.district = district
        self.base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date=".format(district)

    def process(self, date):
        output = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        result = requests.get("{0}{1}".format(self.base, date), headers=headers)
        if (result.status_code == 200):
            data = result.json()
            if not 'centers' in data or len(data['centers']) == 0:
                return output
            for field in data['centers']:
                record = None
                for session in field['sessions']:
                    if self.pincode is None or field['pincode'] == self.pincode:
                        record = [field['name'], 
                                  session['available_capacity'], 
                                  session['vaccine'], 
                                  field['pincode'],
                                  "{}, {}".format(field['block_name'], field['address'])]
                    if record is not None:
                        if self.show is False:
                            output.append(record)
                        else:
                            if session['available_capacity'] > 0:
                                output.append(record)
        else:
            log.error("Got {} response..".format(result.status_code))
                        
        return output