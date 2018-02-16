#!/usr/bin/env python3

import os
import sys
import time
import string
import datetime

def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns the character of the key that was pressed (zero on
    KeyboardInterrupt which can happen when a signal gets handled)

    """
    import termios, fcntl, sys, os
    fd = sys.stdin.fileno()
    # save old state
    flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
    attrs_save = termios.tcgetattr(fd)
    # make raw - the way to do this comes from the termios(3) man page.
    attrs = list(attrs_save) # copy the stored version to update
    # iflag
    attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK 
                  | termios.ISTRIP | termios.INLCR | termios. IGNCR 
                  | termios.ICRNL | termios.IXON )
    # oflag
    attrs[1] &= ~termios.OPOST
    # cflag
    attrs[2] &= ~(termios.CSIZE | termios. PARENB)
    attrs[2] |= termios.CS8
    # lflag
    attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
                  | termios.ISIG | termios.IEXTEN)
    termios.tcsetattr(fd, termios.TCSANOW, attrs)

    # turn off non-blocking
    fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)

    # read a single keystroke
    try:
        ret = sys.stdin.read(1) # returns a single character
    except KeyboardInterrupt: 
        ret = 0
    finally:
        # restore old state
        termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
    return ret


def showTopPicture():
	commandstring = datetime.datetime.now().strftime("gst-launch-1.0 -v v4l2src device=/dev/video1 num-buffers=50 ! textoverlay text='Top Picture' halignment=1 valignment=1 ! 'video/x-raw, width=1920,height=1080,framerate=30/1' ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! tee name=t t. ! queue ! nvtee ! nvoverlaysink t. ! queue ! nvtee ! omxh264enc ! filesink location=./top")
	os.system(commandstring)

def showMiddlePicture():
	commandstring = datetime.datetime.now().strftime("gst-launch-1.0 v4l2src device=/dev/video5 num-buffers=50 ! textoverlay text='Middle Picture' halignment=1 valignment=1 ! 'video/x-raw, width=1920,height=1080,framerate=30/1' ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! tee name=t t. ! queue ! nvtee ! nvoverlaysink t. ! queue ! nvtee ! omxh264enc ! filesink location=./mid")
	os.system(commandstring)

def showBottomPicture():
	commandstring = datetime.datetime.now().strftime("gst-launch-1.0 v4l2src device=/dev/video2 num-buffers=50 ! textoverlay text='Bottom Picture' halignment=1 valignment=1 ! 'video/x-raw, width=1920,height=1080,framerate=30/1' ! nvvidconv ! 'video/x-raw(memory:NVMM)' ! tee name=t t. ! queue ! nvtee ! nvoverlaysink t. ! queue ! nvtee ! omxh264enc ! filesink location=./bot")
	os.system(commandstring)

def takeTopPicture(timestamp, location):
        commandstring = datetime.datetime.now().strftime("gst-launch-1.0 v4l2src device=/dev/video1 num-buffers=1 ! video/x-raw, width=1920,height=1080,framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/media/nvidia/DB3E-9265/" + location + '_top_' + timestamp)
        os.system(commandstring)

def takeMiddlePicture(timestamp, location):
        commandstring = datetime.datetime.now().strftime("gst-launch-1.0 v4l2src device=/dev/video5 num-buffers=1 ! video/x-raw, width=1920,height=1080,framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/media/nvidia/DB3E-9265/" + location + '_mid_' + timestamp)
        os.system(commandstring)

def takeBottomPicture(timestamp, location):
        commandstring = datetime.datetime.now().strftime("gst-launch-1.0 v4l2src device=/dev/video2 num-buffers=1 ! video/x-raw, width=1920,height=1080,framerate=30/1 ! videoconvert ! jpegenc ! filesink location=/media/nvidia/DB3E-9265/" + location + '_bot_' + timestamp)
        os.system(commandstring)


# Set the command 'input' for Python2 or Python3
try:
	input = raw_input
except NameError:
	pass

# Get the store location
location = input('\n\nStore Location: ')

# Loop looking for space character to take photos
while True:
	try:
		showMiddlePicture()
		print("\n\n\nPress space bar to take picture set. 'x' or 's' to quit")
		userInput = read_single_keypress()
		if (userInput == ' '):
			# Take Pictures
			timestamp = datetime.datetime.now().strftime("%y%m%d%H%M%S")
			print("Taking Pictures for " + location)
			takeTopPicture(timestamp, location)
			takeMiddlePicture(timestamp, location)
			takeBottomPicture(timestamp, location)
			print("\n\n2 seconds to move cart\n\n")
			time.sleep(2)
		elif (userInput.upper() == 'S' or userInput.upper() == 'X' or userInput == '0'):
			break
	except KeyboardInterrupt:
		sys.exit()

