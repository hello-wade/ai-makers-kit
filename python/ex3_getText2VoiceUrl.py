#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 3: TTS - getText2VoiceUrl"""

from __future__ import print_function

import aimakerskitutil as aikit
import gigagenieRPC_pb2


CLIENT_ID = 'Y2xpZW50X2lkMTU1MTE0NDE1OTE4NQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTExNDQxNTkxODU='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTExNDQxNTkxODU='

aikit.initClientKey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)

kttts = aikit.getKtApi()

def getText2VoiceUrl(inText):

	message = gigagenieRPC_pb2.reqText()
	message.lang = 0
	message.mode = 0
	message.text = inText

	response = kttts.getText2VoiceUrl(message)
	print ("\n\nresultCd: {}".format(response.resultCd))
	if response.resultCd == 200:
		print ("TTS 생성에 성공하였습니다.\n\n\n아래 URL을 웹브라우져에 넣어보세요.")
		print ("Stream Url: {}\n\n".format(response.url))
	else:
		print ("TTS 생성에 실패하였습니다.")
		print ("Fail: {}".format(response.resultCd))

def main():
	getText2VoiceUrl("안녕하세요 반갑습니다.")

if __name__ == '__main__':
	main()
