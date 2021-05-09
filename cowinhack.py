import os
import time
import click
import traceback
from tabulate import tabulate
from time import sleep
from datetime import datetime
from crawler import crawler


__author__ = "Deepak Patil"

_headers=['State', 'Name', 'Capacity', 'Vaccine', 'PinCode','Address']


@click.group()
def main():
	"""
	LI for starting crawler on co-win to find the available spots, ctrl + C to exit
	"""
	pass


def execute(delay, task, show_available, pincode, district, mute, console):
	next_time = time.time() + delay
	while True:

		try:
			task(show_available, pincode, district, mute, console)
			time.sleep(max(0, next_time - time.time()))
		except Exception:
			traceback.print_exc()
			click.secho('Problem while executing repetitive task.', fg='red', bold=True) 
		# skip tasks if we are behind schedule:
		next_time += (time.time() - next_time) // delay * delay + delay


def say(msg = "Finish", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')


def run(show_available, pincode, district, mute, console):
	date = datetime.today().strftime('%d-%m-%Y')
	try:
		output = crawler(show_available, pincode, district).process(date)
		slot_found = False

		strg = ""
		if len(output) > 0:
			for avail in output:
				strg = "{0} {1}".format(strg, avail[1])
		if len(strg) > 0:
			slot_found = True

		if slot_found or console:
			click.secho("{0} - Slot found.".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S')), fg='green', bold=True) 
			click.secho(tabulate(output, headers=_headers), fg='green', bold=True)
			for i in range(3):
				sleep(3)
				say("Slot found in {0}".format(output[0][0]), "Alex")
		else:
			click.secho("{} - No slot found.".format(datetime.today().strftime('%d-%m-%Y %H:%M:%S')), fg='red', bold=True)
			if mute is False:
				say("No slots found!")

	except Exception as e:
		click.secho("{} - Site is down.".format(datetime.today().strftime('%d-%m-%Y %H:%M:%S')), fg='red', bold=True)
		say("Site is down", "Alex")



@main.command(help='start the crawler')
@click.option('-i', '--interval', required=True, type=int, 
			  help='Interval in seconds.')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
@click.option('-p','--pincode', type=int, help='Provide pincide to start the crawler.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is Thane')
@click.option('-m', '--mute', default=False, is_flag=True,
			  help='Mute repeated announcement if slots are not available, announce only when slots are available.')
@click.option('-c', '--console/--no-console', default=False, is_flag=True,
			  help='Print list of centers even if slots not available.')
def start(interval, show_available, pincode, district, mute, console):
	click.secho('initialising crawler....', fg='cyan') 
	execute(interval, run, show_available, pincode, district, mute, console)


@main.command(help='List down all the centers with address')
@click.option('-p','--pincode', type=int, help='Provide pincide to list the hospitals.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is thane')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
def list(pincode, district, show_available):
	click.secho('listing {} centers for PinCode: {} and District: {}'.format('only the available' if show_available else 'all the', pincode, district), 
			fg='yellow', bold=True)
	try:
		output = crawler(show_available, pincode, district).process(datetime.today().strftime('%d-%m-%Y'))
		if len(output) > 0:
			click.secho(tabulate(output, headers=_headers), fg='yellow', bold=True)
		else:
			click.secho("No centers available...", fg='red', bold=True)
	except Exception as e:
		click.secho("Site is down", fg='red', bold=True)



if __name__ == "__main__":
	main()