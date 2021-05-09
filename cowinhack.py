import click
import traceback
import time

from tabulate import tabulate
from time import sleep
from datetime import datetime
from crawler import crawler

__author__ = "Deepak Patil"

@click.group()
def main():
	"""
	Simple CLI for starting crawler on co-win to find the available spots, ctrl + C to exit
	"""
	pass

def execute(delay, task, show, pincode):
	next_time = time.time() + delay
	while True:
		time.sleep(max(0, next_time - time.time()))
		try:
			task(show, pincode)
		except Exception:
			traceback.print_exc()
			click.secho('Problem while executing repetitive task.', fg='red', bold=True) 
		# skip tasks if we are behind schedule:
		next_time += (time.time() - next_time) // delay * delay + delay
	

def run(show, pincode):
	msg = "fetching data form cowin for {0}....".format(datetime.today().strftime('%d-%B-%Y %H:%M:%S'))
	click.secho(msg, fg='yellow', bold=True) 
	date = datetime.today().strftime('%d-%m-%Y')
	output = crawler(show, pincode).start_process(date)
	if len(output) > 0:
		click.secho(tabulate(output, headers=['Name', 'Capacity', 'Vaccine', 'Address']), fg='yellow', bold=True)
	else:
		click.secho("Not slot found... will try again!", fg='red', bold=True)


@main.command(help='start the crawler')
@click.option('-i', '--interval', required=True, type=int, 
			  help='Interval in seconds.')
@click.option('-t', '--show/--no-show', default=False, 
			  help='Track availablilty of region even if the available capacity is zero.')
@click.option('-p','--pincode', required=True, type=int,
			  help='Provide pincide to start the crawler.')
def start(interval, show, pincode):
	click.secho('initialising crawler....', fg='cyan') 
	execute(interval, run, show, pincode)


@main.command(help='List down all the centers with address')
@click.option('-p','--pincode', type=int, help='Provide pincide to list the hospitals.')
def list(pincode):

	click.secho('listing all the centers....', fg='yellow', bold=True)
	date = datetime.today().strftime('%d-%m-%Y')
	output = crawler(False, pincode).list_centers(date)
	if len(output) > 0:
		click.secho(tabulate(output, headers=['PinCode', 'Center Id', 'Name & Address']), fg='yellow', bold=True)
	else:
		click.secho("No centers available...", fg='red', bold=True)



if __name__ == "__main__":
	main()