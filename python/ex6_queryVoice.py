#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 6: STT + Dialog - queryByVoice"""

from __future__ import print_function

import aimakerskitutil as aikit
import gigagenieRPC_pb2

### STT
import pyaudio
import audioop
from gkit._audio import *


import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

CLIENT_ID = 'Y2xpZW50X2lkMTU1MTE0NDE1OTE4NQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTExNDQxNTkxODU='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTExNDQxNTkxODU='

aikit.initClientKey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)

query = aikit.getKtApi()

def generateRequest():
	with MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		messageReq = gigagenieRPC_pb2.reqQueryVoice()
		messageReq.reqOptions.lang=0
		messageReq.reqOptions.userSession="1234"
		messageReq.reqOptions.deviceId="totallyrandomdeviceid"
		yield messageReq
		for content in audio_generator:
			message = gigagenieRPC_pb2.reqQueryVoice()
			message.audioContent = content
			yield message

def queryByVoice():
	print ("\n\n\n질의할 내용을 말씀해 보세요.\n\n듣고 있는 중......\n")
	request = generateRequest()
	resultText = ''
	response = query.queryByVoice(request)
	if response.resultCd == 200:
		print("질의 내용: %s" % (response.uword))
		for a in response.action:
			response = a.mesg
			parsingResp = response.replace('<![CDATA[', '').replace(']]>', '')
			resultText = parsingResp
			print("\n질의에 대한 답변: {} \n\n\n".format(parsingResp))

	else:
		print("\n\nresultCd: %d\n" % (response.resultCd))
		print("정상적인 음성인식이 되지 않았습니다.")

	return resultText

def main():
	queryByVoice()
	time.sleep(0.5)

if __name__ == '__main__':
	main()
