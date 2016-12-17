#!C:\Users\Wojtek\AppData\Local\Programs\Python\Python35-32\python
# -*- coding: utf-8 -*-
import cgi, os

home = "C:\\Users\\Wojtek\\Desktop\\Pomoce\\Apache\\Apache24\\htdocs"
contentType = "Content-Type: text/html\r\n\r\n"
contentTypeJson = "Content-Type: application/json\r\n\r\n"
	
def sendResponse(text):
	print(contentType + text)
	
def sendJSONResponse(text):
	print(contentTypeJson + text)
	
def sendError(number, reason):
	print("Status: " + str(number) + " " + reason + "\r\n" + contentType)

def getMethod():
	return os.environ["REQUEST_METHOD"]