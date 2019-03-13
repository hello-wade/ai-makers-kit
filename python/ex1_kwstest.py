#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 1: GiGA Genie Keyword Spotting"""

from __future__ import print_function

import pyaudio
import audioop
import RPi.GPIO as GPIO
import ktkws
import aimakerskitutil as aikit
import gkit._audio as gkitAudio


KWSID = ['기가지니', '지니야', '친구야', '자기야']

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
btnStatus = False

def callback(channel):
	print("falling edge detected from pin {}".format(channel))
	global btnStatus
	btnStatus = True
	print(btnStatus)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

def detect():
	with gkitAudio.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:

			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))

			if (rc == 1):
				gkitAudio.playWav("../data/sample_sound.wav")
				return 200

def detectButton():
	global btnStatus
	rc = 10 # Start rc
	while True:
		GPIO.output(31, GPIO.HIGH)
		if (btnStatus == True):
			rc = 1
			btnStatus = False
		if (rc == 1):
			GPIO.output(31, GPIO.LOW)
			gkitAudio.playWav("../data/sample_sound.wav")
			return 200
			break

def test(keyWord = '기가지니'):
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = {}'.format(rc))
	rc = ktkws.start()
	print ('start rc = {}'.format(rc))
	print ('\n호출어를 불러보세요~\n')
	ktkws.set_keyword(KWSID.index(keyWord))
	rc = detect()
	print ('detect rc = {}'.format(rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

def btnTest():
	print ('\n버튼을 눌러보세요~\n')
	global btnStatus
	rc = detectButton()
	print ('detect rc = {}'.format(rc))
	print ('\n\n버튼이 정상적으로 인식되었습니다.\n\n')
	return rc

def main():
	btnTest()

if __name__ == '__main__':
	main()