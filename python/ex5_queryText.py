#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 5: Dialog - queryByText"""

from __future__ import print_function

import aimakerskitutil as aikit
import gigagenieRPC_pb2

CLIENT_ID = 'Y2xpZW50X2lkMTU1MTE0NDE1OTE4NQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTExNDQxNTkxODU='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTExNDQxNTkxODU='

aikit.initClientKey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)

query = aikit.getKtApi()

# DIALOG : queryByText
def queryByText(text):
	message = gigagenieRPC_pb2.reqQueryText()
	message.queryText = text
	message.userSession = "1234"
	message.deviceId = "yourdevice"
	response = query.queryByText(message)

	print ("\n\nresultCd: {}".format(response.resultCd))
	if response.resultCd == 200:
		print ("\n\n\n질의한 내용: {}".format(response.uword))
		
		answer = response.action[0].mesg

		parsedAnswer = answer.replace('<![CDATA[', '').replace(']]>', '')
		print("\n\n질의에 대한 답변: {} \n\n\n".format(parsedAnswer))
	else:
		print ("Fail: {}".format(response.resultCd))

def main():

	# Dialog : queryByText
	queryByText("안녕")

if __name__ == '__main__':
	main()
