import os
import time
import click
import traceback
from tabulate import tabulate
from time import sleep
from datetime import datetime
from crawler import crawler


__author__ = "Deepak Patil"

_headers=['Name', 'Capacity', 'Vaccine', 'PinCode','Address']


@click.group()
def main():
	"""
	LI for starting crawler on co-win to find the available spots, ctrl + C to exit
	"""
	pass


def execute(delay, task, show_available, pincode, district, speak_on_available, console):
	next_time = time.time() + delay
	while True:
		time.sleep(max(0, next_time - time.time()))
		try:
			task(show_available, pincode, district, speak_on_available, console)
		except Exception:
			traceback.print_exc()
			click.secho('Problem while executing repetitive task.', fg='red', bold=True) 
		# skip tasks if we are behind schedule:
		next_time += (time.time() - next_time) // delay * delay + delay


def say(msg = "Finish", voice = "Victoria"):
    os.system(f'say -v {voice} {msg}')


def run(show_available, pincode, district, speak_on_available, console):
	msg = "fetching data form cowin for {0}....".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S'))
	click.secho(msg, fg='yellow', bold=True) 
	date = datetime.today().strftime('%d-%m-%Y')
	output = crawler(show_available, pincode, district).process(date)

	slot_found = False
	for avail in output:
		if avail[1] > 0:
			slot_found = True
			break;

	if slot_found or console:
		click.secho(tabulate(output, headers=_headers), fg='yellow', bold=True)

	if slot_found:
		for i in range(5):
			sleep(2)
			say("Slot found, book the appointment", "Alex")
	else:
		click.secho("No slot found... will try again!", fg='red', bold=True)
		if speak_on_available is False:
			say("No slots found!")



@main.command(help='start the crawler')
@click.option('-i', '--interval', required=True, type=int, 
			  help='Interval in seconds.')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
@click.option('-p','--pincode', type=int, help='Provide pincide to start the crawler.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is Thane')
@click.option('-a', '--speak-on-available', default=False, is_flag=True,
			  help='Announce only when slots are available.')
@click.option('-c', '--console/--no-console', default=False, is_flag=True,
			  help='Print list of centers even if slots not available.')
def start(interval, show_available, pincode, district, speak_on_available, console):
	click.secho('initialising crawler....', fg='cyan') 
	execute(interval, run, show_available, pincode, district, speak_on_available, console)


@main.command(help='List down all the centers with address')
@click.option('-p','--pincode', type=int, help='Provide pincide to list the hospitals.')
@click.option('-d','--district', type=int, default=392,
			  help='Provide district code to filter the crawler, default is thane')
@click.option('-s', '--show-available', is_flag=True, default=False, help='List all centers only if slots are available.')
def list(pincode, district, show_available):
	click.secho('listing {} centers for PinCode: {} and District: {}'.format('only the available' if show_available else 'all the', pincode, district), 
			fg='yellow', bold=True)
	output = crawler(show_available, pincode, district).process(datetime.today().strftime('%d-%m-%Y'))
	if len(output) > 0:
		click.secho(tabulate(output, headers=_headers), fg='yellow', bold=True)
	else:
		click.secho("No centers available...", fg='red', bold=True)



if __name__ == "__main__":
	main()