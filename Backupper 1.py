import tkinter.filedialog
import sys, time, msvcrt
from shutil import copy2

ventetid = 1

# Intellectual property of Torleif Hensvold
# Permission to freely distribute this script in its unaltered form (that includes comments) is granted in perpetuity.
# This script is provided as-is and the user takes full responsibility for any and all damages caused by this script.

def runningLoop(tid, filename, location, backuplocation):
	# This starts a backup immediately, then repeats at a given time interval until the user presses a key in
	# the console window, whereupon a last backup is generated and the script exits.
	backup(filename, location, backuplocation)
	countdown = tid
	while not msvcrt.kbhit():		# While we haven't gotten a keyboard input, do the following lines
		time.sleep(5)				# sleep for 5 seconds
		countdown = countdown - 5	# subtract 5 seconds from the time until backup
		#print(countdown)			# Testing artefact
		if countdown <= 0:			# if we're at the time we should've made a backup within 5 seconds
			backup(filename, location, backuplocation)	# Do the backup
			countdown = tid			# And then we reset the countdown timer and start again
	backup(filename, location, backuplocation)
	print("Backup Ended")
	print("Closing window in:")
	for i in reversed(range(20)):
		print(i)
		time.sleep(1)


def backup(filename, location, backuplocation):
	timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
	delt = filename.split(".")
	backupfilename = delt[0] + "_" + timestamp + "." + delt[1]
	copy2(location, backuplocation + "/" + backupfilename)
	print("Made backup at " + timestamp)


def tidssplitter(tid):
	mellom = tid.split()
	if len(mellom) > 4:
		return 5, 0
	elif len(mellom) == 4:
		return mellom[0], mellom[2]
	elif len(mellom) == 2:
		if mellom[1] == ("m"):
			return mellom[0], 0
		elif mellom[1] == ("s"):
			return 0, mellom[0]
		else:
			return 5, 0
	else:
		return 5, 0


def tidskonverterToSeconds(minutter, sekunder):		# Converts from minutes and seconds to only seconds
	plussSekunder = 60 * minutter
	total = sekunder + plussSekunder
	return total

def fiksTid(tid):						# calls the functions to make sure we have a time for backups
	minutter, sekunder = tidssplitter(tid)
	sekundtid = tidskonverterToSeconds(int(minutter), int(sekunder))
	return sekundtid

print("What file do you want to keep backing up?")
time.sleep(ventetid)
filelocation = tkinter.filedialog.askopenfilename()
perten = str(filelocation)
perten = perten.split("/")
filename = perten[-1]
print(filename)
print("We found your chosen file to be at: " + filelocation)

print("\nWhere do you want to keep the backed up files?")
time.sleep(ventetid)
backuplocation = tkinter.filedialog.askdirectory()
print("We found your chosen backup folder to be: " + backuplocation)

print("\nHow often do you want the backup to run?")
print("Answer on the form '_ m _ s' where m is minutes and s is seconds")
print("This program will behave unexpectedly unless given proper input.")
tidsinput = input()
print()

# TODO: add message printing the time interval between backups.

runningLoop(fiksTid(tidsinput), filename, filelocation, backuplocation)
