#!C:\Program Files\Anaconda3\python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-
import cgi, os, subprocess
from _pomoc import sendJSONResponse, sendError, home
import threading
import json

import numpy as np
import parse_result as pr

import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

method = os.environ["REQUEST_METHOD"]

if (method == "POST"):
	form = cgi.FieldStorage()
	netlist = form.getfirst("netlist", "")	
	id = threading.get_ident()
	
	inFile = "in" + str(id) + ".txt"
	inPath = home + "/tmp/" + inFile
	outFile = "out" + str(id) + ".txt"
	outPath = home + "/tmp/" + outFile
	
	#try:
	file = open(inPath, "w")
	file.write(netlist)
	file.close()
	
	qucs = subprocess.Popen(["skrypt.bat", inFile, outFile],stdout=subprocess.PIPE)
	res = qucs.communicate()
	if os.path.isfile(outPath):
		#"creating netlist..." in str(res):
		data = pr.parse_file(outPath)
		sendData = {}
		for key in data:
			if isinstance(data[key], dict):
				sendData[key] = data[key]
			else:
				sendData[key] = []				
				for num in range(len(data[key])):
					i = data[key][num]
					if isinstance(i, complex):
						sendData[key].append("c" + str(i))
					else:
						sendData[key].append(str(i))
		sendJSONResponse(json.dumps(sendData))
		#file = open(outPath, "r")
		#data = ""
		#for line in file:
		#	data += line
		#file.close()
		#sendJSONResponse('{"status":"' + data + '"}')
		os.remove(outPath)
	else:
		sendError(400, "Bad Request")
	os.remove(inPath)
	#except:
	#	os.remove(outPath)
	#	os.remove(inPath)
	#	sendError(401, "Bad Request")
	#qucs = subprocess.Popen(["qucs\\qucsator.exe", "-i tmp\\in.txt", "-o tmp\\out.txt"],stdout=subprocess.PIPE)
else:
	sendError(405, "Method Not Allowed")