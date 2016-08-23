#!/usr/bin/python3
#Helper Script to make a valid list of PRNs 
import requests
import PyPDF2
import os

examCodes = ['43', '44', '45', '46', '47', '48', '49']
examCode = 1
prnBeg = 13000000
prnSpan = 30000
prnEnd = prnBeg + prnSpan
url = "http://projects.mgu.ac.in/bTech/btechresult/index.php?module=public&attrib=result&page=result"
headers = {
	    'content-type': "multipart/form-data; boundary=---011000010111000001101001",
	    'cache-control': "no-cache"
	    }
lastValidPRN = 0
lastInValidPRN = 0
for prn in range(prnBeg, prnEnd):
	payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"exam\"\r\n\r\n" + examCodes[examCode] +"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prn\"\r\n\r\n" + str(prn) +"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"Submit2\"\r\n\r\nSubmit\r\n-----011000010111000001101001--"
	response = requests.request("POST", url, data=payload, headers=headers)
	if(response.text[1:4]=='PDF'):
		file = open("list.txt", "a")
		file.write(str(prn) + "\n")
		print( "VALID: " + str(prn))
		lastValidPRN = str(prn)
		file.close()
	else:
		print(str(prn)+ ":INVALID")
		lastInValidPRN = str(prn)
print("LAST VALID PRN: " + lastValidPRN)
print("LAST INVALID PRN: " + lastInValidPRN)
print("Valid PRN List Made!...Time to Run the < Scrapper > Happy Scraping!")