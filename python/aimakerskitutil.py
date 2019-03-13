# -*- coding: utf-8 -*-

from __future__ import print_function

# gRPC
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

# creadentials
import datetime
import hmac
import hashlib

# Error Hander
from six.moves import queue
from ctypes import *



CLIENT_ID = ''
CLIENT_KEY = ''
CLIENT_SECRET = ''
HOST = 'gate.gigagenie.ai'
PORT = 4080
SSLCERTFILE = '../data/ca-bundle.pem'


def initClientKey(clientID, clientKey, clientSecret):
    global CLIENT_ID
    global CLIENT_KEY
    global CLIENT_SECRET

    CLIENT_ID = clientID
    CLIENT_KEY = clientKey
    CLIENT_SECRET = clientSecret

def getKtApi():
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

    return stub

def getMetadata():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + timestamp

    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()

    metadata = [('x-auth-clientkey', CLIENT_KEY),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]

    return metadata

def credentials(context, callback):
    callback(getMetadata(), None)

def getCredentials():
    with open(SSLCERTFILE, 'rb') as f:
        trusted_certs = f.read()
    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    authCred = grpc.metadata_call_credentials(credentials)

    return grpc.composite_channel_credentials(sslCred, authCred)


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)
