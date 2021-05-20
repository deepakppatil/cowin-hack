import logging
import traceback
import requests
import datetime
import time

__author__ = "Deepak Patil"

from tabulate import tabulate
from time import sleep

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
log = logging.getLogger('__name__')
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.DEBUG)

class crawler:

	def __init__(self, pincode, district):
		self.pincode = pincode
		self.district = district
		# self.base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date=".format(district)
		self.base = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={}&date=".format(district)

		# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiIyZGI3M2JmYi0yMjc1LTRjYzgtYmY0MS1jNzcxYjcwNGIyZWEiLCJ1c2VyX2lkIjoiMmRiNzNiZmItMjI3NS00Y2M4LWJmNDEtYzc3MWI3MDRiMmVhIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5OTMwODcwMjk5LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjM5Mzg2NTMyOTEwNzcsInNlY3JldF9rZXkiOiJiNWNhYjE2Ny03OTc3LTRkZjEtODAyNy1hNjNhYTE0NGYwNGUiLCJ1YSI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzYpIEFwcGxlV2ViS2l0LzYwNS4xLjE1IChLSFRNTCwgbGlrZSBHZWNrbykgVmVyc2lvbi8xNC4wLjMgU2FmYXJpLzYwNS4xLjE1IiwiZGF0ZV9tb2RpZmllZCI6IjIwMjEtMDUtMTlUMjA6NDk6MDIuMjM0WiIsImlhdCI6MTYyMTQ1NzM0MiwiZXhwIjoxNjIxNDU4MjQyfQ.1upIg-cf0fVlwLIk1Mp0nRjOnBVm3l4YloODekpv3dU'
	
	def process(self, date, min_age, max_age, show_available, token):

		output = []

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
					   'Authorization': 'Bearer {}'.format(token),
					   'referer': 'https://selfregistration.cowin.gov.in/',
					   'origin': 'https://selfregistration.cowin.gov.in'
			}
			url = "{0}{1}".format(self.base, date)
			log.debug(url)

			try:
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
			except Exception as ex:
				raise ex
			finally:
				log.debug("Got {} response..".format(result.status_code))

			if (result.status_code == 200):
				data = result.json()
				if not 'centers' in data or len(data['centers']) == 0:
					return

				for field in data['centers']:
					record = None
					for session in field['sessions']:
						record = [session['date'],
								  field['state_name'],
								  field['pincode'],
								  field['name'], 
								  session['available_capacity_dose1'],
								  session['available_capacity_dose2'], 
								  session['vaccine'],
								  session['min_age_limit'],
								  session['slots']
								  ]
								  #"{}".format(field['address'])]
						if show_available and int(session['available_capacity']) > 0 and (self.pincode is None or field['pincode'] == self.pincode) and session['min_age_limit'] >= min_age and session['min_age_limit'] <= max_age:
							output.append(record)
						elif show_available is False and (self.pincode is None or field['pincode'] == self.pincode) and session['min_age_limit'] >= min_age and session['min_age_limit'] <= max_age:
							output.append(record)
						else:
							continue

		except Exception as ex:
			log.debug("Got {} response..".format(result.status_code))
		finally:
			return output