import logging
import traceback
import requests
import time

__author__ = "Deepak Patil"

from tabulate import tabulate
from time import sleep
from datetime import datetime

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
log = logging.getLogger('__name__')
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

class crawler:

    def __init__(self, show_available, pincode, district):
        self.show = show_available
        self.pincode = pincode
        self.district = district
        self.base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date=".format(district)
        
    def process(self, date):
        output = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'}
        
        try:
            url = "{0}{1}".format(self.base, date)
            # log.info(url)
            result = requests.get(url, headers=headers, timeout=5)
        except requests.exceptions.Timeout as e: 
            raise e
        except requests.exceptions.RequestException as err:
            raise err
        except requests.exceptions.HTTPError as errh:
            raise errh
        except requests.exceptions.ConnectionError as errc:
            raise errc
        except requests.exceptions.Timeout as errt:
            raise errt

        log.debug("Got {} response..".format(result.status_code))
        if (result.status_code == 200):
            data = result.json()
            if not 'centers' in data or len(data['centers']) == 0:
                return output
            for field in data['centers']:
                record = None
                for session in field['sessions']:
                    if self.pincode is None or field['pincode'] == self.pincode:
                        record = [field['state_name'],
                                  field['name'], 
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