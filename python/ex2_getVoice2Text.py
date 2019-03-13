#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

import aimakerskitutil as aikit
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import gkit._audio as gkitAudio
import pyaudio
import audioop

CLIENT_ID = 'Y2xpZW50X2lkMTU1MTE0NDE1OTE4NQ=='
CLIENT_KEY = 'Y2xpZW50X2tleTE1NTExNDQxNTkxODU='
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldDE1NTExNDQxNTkxODU='

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

aikit.initClientKey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)


ktstt = aikit.getKtApi()

def generateRequest():

    with gkitAudio.MicrophoneStream(RATE, CHUNK) as stream:
        audioGenerator = stream.generator()

        for content in audioGenerator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message

def getVoice2Text():
    print ("\n\n음성인식을 시작합니다.\n\n종료하시려면 Ctrl+\ 키를 누루세요.\n\n\n")

    request = generateRequest()
    resultText = ''
    for response in ktstt.getVoice2Text(request):
        if response.resultCd == 200: # partial
            print('resultCd= {} | recognizedText= {}'
                .format(response.resultCd, response.recognizedText))
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            print('resultCd= {} | recognizedText= {}'
                  .format(response.resultCd, response.recognizedText))
            resultText = response.recognizedText
            break
        else:
            print('resultCd= {} | recognizedText= {}'
                  .format(response.resultCd, response.recognizedText))
            break

    return resultText


def main():
    text = getVoice2Text()
    print ("인식결과: {}".format(text))

if __name__ == '__main__':
    main()