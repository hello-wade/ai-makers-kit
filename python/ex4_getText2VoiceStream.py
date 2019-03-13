#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 4: TTS - getText2VoiceStream"""

from __future__ import print_function

import aimakerskitutil as aikit
import gigagenieRPC_pb2
import gkit._audio as gkitAudio

CLIENT_ID = 'Y2xpZW50X2lkMTU1MTE0NDE1OTE4NQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTExNDQxNTkxODU='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTExNDQxNTkxODU='

aikit.initClientKey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)

kttts = aikit.getKtApi()

def getText2VoiceStream(inText,inFileName):

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText

	writeFile=open(inFileName,'wb')
	for response in kttts.getText2VoiceStream(message):
		if response.HasField("resOptions"):
			print ("\n\nResVoiceResult: {}".format(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	return response.resOptions.resultCd

def main():
	fileName = "testtts.wav"
	getText2VoiceStream("안녕하세요. 반갑습니다.", fileName)
	gkitAudio.playWav(fileName)
	print(fileName + "이 생성되었으니 파일을 확인바랍니다. \n\n\n")


if __name__ == '__main__':
	main()
