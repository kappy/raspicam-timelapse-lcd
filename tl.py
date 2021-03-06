#!/usr/bin/python

import time
import datetime
import os
import picamera
import Adafruit_CharLCD as LCD

FRAMES_PER_HOUR = 6
UPDATE_SECONDS = 5
ROTATION = 90

lcd = LCD.Adafruit_CharLCDPlate()

def calculate_seconds_to_next(start):
    seconds = int(60 * 60 / FRAMES_PER_HOUR) - (time.time() - start)
    return seconds - seconds % UPDATE_SECONDS

def capture_frame(path, frame):
    lcd.clear()
    lcd.message('Shooting #%03d' % frame)
    with picamera.PiCamera() as cam:
        cam.rotation = ROTATION
	cam.resolution = (1920, 1080)
	cam.framerate = 30
    # Give the camera's auto-exposure and auto-white-balance algorithms
    # some time to measure the scene and determine appropriate values
    	cam.ISO = 200
    	time.sleep(2)
    	# Now fix the values
    	cam.shutter_speed = cam.exposure_speed
    	#cam.exposure_mode = 'off'
   	g = cam.awb_gains
    	cam.awb_mode = 'off'
	cam.awb_gains = g
        time.sleep(2)
        cam.capture('%s/frame%03d.jpg' % (path, frame))

def time_lapse():
    #create directory with date
    date = datetime.datetime.now().strftime('%Y%m%d')
    directory = '/home/pi/%s' % date
    if not os.path.exists(directory):
        os.makedirs(directory)

    frame = 0
    # Capture the images
    while True:
        # Note the time before the capture
        frame = frame + 1
        start = time.time()
        capture_frame(directory, frame)
        # Wait for the next capture. Note that we take into
        # account the length of time it took to capture the
        # image when calculating the delay
        while True:
            seconds_to_next = calculate_seconds_to_next(start)
            if seconds_to_next <= 0:
                break
            lcd.clear()
            lcd.message('taken: %03d\n' % frame)
            lcd.message('next: %s' % str(datetime.timedelta(seconds=seconds_to_next)))
            while calculate_seconds_to_next(start) == seconds_to_next :
                if lcd.is_pressed(LCD.SELECT):
                    return
            #time.sleep(1)

while True:
    lcd.clear()
    lcd.message('Press SELECT to\n start...')
    while True:
        if not lcd.is_pressed(LCD.SELECT):
            continue
	break
    time_lapse()

