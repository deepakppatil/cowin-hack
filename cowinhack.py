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

_headers=['Date', 'State', 'Name', 'Capacity', 'Vaccine', 'PinCode','Address']


@click.group()
def main():
	"""
	LI for starting crawler on co-win to find the available spots, ctrl + C to exit
	"""
	pass


def execute(delay, task, show_available, pincode, district, mute, console, start_date, no_days):
	next_time = time.time() + delay
	while True:

		try:
			task(show_available, pincode, district, mute, console, start_date, no_days)
			time.sleep(max(0, next_time - time.time()))
		except Exception:
			traceback.print_exc()
			click.secho('Problem while executing repetitive task.', fg='red', bold=True) 
		# skip tasks if we are behind schedule:
		next_time += (time.time() - next_time) // delay * delay + delay


def say(msg = "Finish", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')


def run(show_available, pincode, district, mute, console, start_date, no_days):
	# date = datetime.today().strftime('%d-%m-%Y')
	date = start_date.strftime('%d-%m-%Y')
	try:
		output = crawler(show_available, pincode, district, no_days).process(date)
		slot_found = False
		empty = True
		for ox in output:
			empty = False
			if ox[3] > 0:
				slot_found = True
				break

		if slot_found or console and empty is False:
			click.secho("{0} - Slot found.".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S')), 
				fg='green', bold=True) 
			click.secho(tabulate(output, headers=_headers), fg='green', bold=True)
			for i in range(3):
				sleep(3)
				say("Slot found in {0}".format(output[0][1]), "Alex")
		else:
			if mute is False:
				say("No slots found!")
				click.secho("{0} - No slot found.".format(datetime.today().strftime('%d-%m-%Y %H:%M:%S')), 
					fg='red', bold=True)

	except Exception as e:
		click.secho("{} - exception: {}".format(e), fg='red', bold=True)
		say("API is unavailable", "Alex")


@main.command(help='start the crawler')
@click.option('-i', '--interval', required=True, type=int, 
			  help='Interval in seconds.')
@click.option('-s', '--show-available', is_flag=True, default=False, 
			  help='List all centers only if slots are available.')
@click.option('-p','--pincode', type=int, help='Provide pincide to start the crawler.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is Thane')
@click.option('-m', '--mute', default=False, is_flag=True,
			  help='Mute repeated announcement if slots are not available, announce only when slots are available.')
@click.option('-c', '--console/--no-console', default=False, is_flag=True,
			  help='Print list of centers even if slots not available.')
@click.option('-sd', '--start-date', type=click.DateTime(formats=["%d-%m-%Y"]), default=date.today().strftime("%d-%m-%Y"),
			  help='Starting date, default=T.')
@click.option('-nd', '--no-days', type=int, default=3,
			  help='No of days from T, default=T+3.')
def start(interval, show_available, pincode, district, mute, console, start_date, no_days):
	click.secho('crawler initialised....', fg='cyan') 
	execute(interval, run, show_available, pincode, district, mute, console, start_date, no_days)


@main.command(help='List down all the centers with address')
@click.option('-p','--pincode', type=int, help='Provide pincide to list the hospitals.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is thane')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
@click.option('-sd', '--start-date', type=click.DateTime(formats=["%d-%m-%Y"]), default=date.today().strftime("%d-%m-%Y"),
			  help='Starting date, default=T.')
@click.option('-nd', '--no-days', type=int, default=3,
			  help='No of days from T, default=T+3.')
def list(pincode, district, show_available, start_date, no_days):
	click.secho('listing {} centers for PinCode: {} and District: {}'.format('only the available' if show_available else 'all the', pincode, district), 
			fg='yellow', bold=True)
	try:
		date = start_date.strftime('%d-%m-%Y')
		output = crawler(show_available, pincode, district, no_days).process(date)
		if len(output) > 0:
			click.secho(tabulate(output, headers=_headers), fg='yellow', bold=True)
		else:
			click.secho("No centers available...", fg='red', bold=True)
	except Exception as e:
		click.secho("Site is down", fg='red', bold=True)



if __name__ == "__main__":
	main()