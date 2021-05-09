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

    # base url
    base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=392&date="

    def __init__(self, show, pincode, announce=False):
        log.debug("__inside__")
        self.show = show
        self.pincode = pincode
        self.announce = announce
        
        
    def start_process(self, date):
        """
        function the data from cowin
        """
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        result = requests.get("{0}{1}".format(self.base, date), headers=headers)
        if (result.status_code == 200):
            return self.churn(result.json())
        else:
            log.error("Got {} response..".format(result.status_code))
            return []
    
    def churn(self, data):
        output = []
        for field in data['centers']:
            if field['pincode'] == self.pincode:
                for session in field['sessions']:
                    record = [field['name'], 
                                  session['available_capacity'], 
                                  session['vaccine'], 
                                  "{}, {}".format(field['block_name'], field['address'])]
                    if session['available_capacity'] > 0 or self.show:
                        output.append(record)
                        
        return output

    def list_centers(self, date):
        """
        function the data from cowin
        """
        output = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        result = requests.get("{0}{1}".format(self.base, date), headers=headers)
        if (result.status_code == 200):
            data = result.json()
            for field in data['centers']:
                if field['pincode'] == self.pincode or self.pincode is None:
                    addr = "{}: {}, {}".format(field['name'], field['block_name'], field['address'])
                    output.append([field['pincode'], field['center_id'], addr])
            return output