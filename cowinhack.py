#changes
import os
import time
import click
import traceback

from datetime import date
from tabulate import tabulate
from time import sleep
from datetime import datetime
from crawler import crawler



__author__ = "Deepak Patil"

_headers=['Date', 'District', 'PinCode', 'Name', 'Dose1', 'Dose2', 'Vaccine', 'Age', 'slots']


@click.group()
def main():
	"""
	LI for starting crawler on co-win to find the available spots, ctrl + C to exit
	"""
	pass


def execute(delay, task, show_available, pincode, district, mute, console, start_date, age, token, dose):
	next_time = time.time() + delay
	while True:

		try:
			task(show_available, pincode, district, mute, console, start_date, age, token, dose)
			time.sleep(max(0, next_time - time.time()))
		except Exception:
			traceback.print_exc()
			click.secho('Problem while executing repetitive task.', fg='red', bold=True) 
		# skip tasks if we are behind schedule:
		next_time += (time.time() - next_time) // delay * delay + delay


def say(msg = "Finish", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')


def run(show_available, pincode, district, mute, console, start_date, age, token, dose):
	date = start_date.strftime('%d-%m-%Y')
	try:
		min_age, max_age = get_age(age)
		output = crawler(pincode, district).process(date, min_age, max_age, show_available, token)
		slot_found_d1, slot_found_d2, empty1, empty2 = False, False, True, True
		total_slots_d1, total_slots_d2 = 0, 0
		op_dose1, op_dose2 = [], []

		for y in output:
			if y[4] > 0:
				empty1 = False
				total_slots_d1 = y[4] + total_slots_d1 
				op_dose1.append(y)

			if y[5] > 0:
				empty2 = False
				total_slots_d2 = y[5] + total_slots_d2
				op_dose2.append(y)
				slot_found_d1 = True

		if slot_found_d1 and empty1 is False and (dose == '0' or dose == '1'):
			click.secho("\n")
			msg = "{0} dose1 slots found in {1} for {2}+ age".format(total_slots_d1, output[0][1], age)
			click.secho("{0} - {1}".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S'), msg), fg='cyan', bold=True) 
			if total_slots_d1 > 0 or console:
				click.secho(tabulate(op_dose1, headers=_headers), fg='green', bold=True)
			if mute is False:
				say(msg, "Alex")
		else:
			# if mute is False:
				# say("No slots found!")
			click.secho("{0} - Dose1 No slot found.".format(datetime.today().strftime('%d-%m-%Y %H:%M:%S')), fg='red', bold=True)

		if slot_found_d2 and empty2 is False and (dose == '0' or dose == '2'):
			msg = "{0} dose2 slots found in {1} for {2}+ age".format(total_slots_d2, output[0][1], age)
			click.secho("{0} - {1}".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S'), msg),  fg='cyan', bold=True) 
			if total_slots_d2 > 0 or console:
				click.secho(tabulate(op_dose2, headers=_headers), fg='green', bold=True)
			if mute is False:
				say(msg, "Alex")
		else:
			# if mute is False:
			# 	#say("No slots found!")
			click.secho("{0} - Dose2 No slot found.".format(datetime.today().strftime('%d-%m-%Y %H:%M:%S')), fg='red', bold=True)
				

	except Exception as e:
		click.secho("{} - exception: {}".format(e), fg='red', bold=True)
		say("API is unavailable", "Alex")
		raise Exception


@main.command(help='start the crawler')
@click.option('-i', '--interval', required=True, type=int, 
			  help='Interval in seconds.')
@click.option('-s', '--show-available', is_flag=True, default=False, 
			  help='List all centers only if slots are available.')
@click.option('-p','--pincode', type=int, default=None, help='Provide pincide to start the crawler.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is Thane')
@click.option('-m', '--mute', default=False, is_flag=True,
			  help='Mute repeated announcement if slots are not available, announce only when slots are available.')
@click.option('-c', '--console/--no-console', default=False, is_flag=True,
			  help='Print list of centers regardless of availablilty.')
@click.option('-dt', '--date', type=click.DateTime(formats=["%d-%m-%Y"]), default=date.today().strftime("%d-%m-%Y"),
			  help='Starting date, default=T.')
@click.option('-a', '--age', type=click.Choice(['18', '45']), default="18", help='Min age limit.')
@click.option('-t','--token', type=str, default=None, help='Provide access token.')
@click.option('-vd', '--dose', type=click.Choice(['1', '2', '0']), default='0', help='Dose 1, Dose 2, select 0 for all.')
def start(interval, show_available, pincode, district, mute, console, date, age, token, dose):
	click.secho('crawler initialised...', fg='cyan')
	
	if console: 
		show_available = False

	execute(interval, run, show_available, pincode, district, mute, console, date, age, token, dose)


@main.command(help='List down all the centers with address')
@click.option('-p','--pincode', type=int, default=None, help='Provide pincide to list the hospitals.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is thane')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
@click.option('-dt', '--date', type=click.DateTime(formats=["%d-%m-%Y"]), default=date.today().strftime("%d-%m-%Y"),
			  help='Starting date, default=T.')
@click.option('-a', '--age', type=click.Choice(['18', '45']), default="18", help='Min age limit.')
@click.option('-t','--token', type=str, default=None, help='Provide access token.')
def list(pincode, district, show_available, date, age, token):
	click.secho('listing {} centers for PinCode: {} and District: {}'.format('only the available' if show_available else 'all the', pincode, district), 
			fg='yellow', bold=True)
	try:
		min_age, max_age = get_age(age)
		output = crawler(pincode, district).process(date.strftime('%d-%m-%Y'), min_age, max_age, show_available, token)
		
		if len(output) > 0:
			click.secho(tabulate(output, headers=_headers), fg='yellow', bold=True)
		else:
			click.secho("No centers available...", fg='red', bold=True)
	except Exception as e:
		click.secho(e, fg='red', bold=True)
		click.secho("Site is down", fg='red', bold=True)


def get_age(min_age_limit):
	if min_age_limit == "18":
		min_age = 18
		max_age = 44
	else:
		min_age = 45
		max_age = 120	
	return min_age, max_age

if __name__ == "__main__":
	main()
