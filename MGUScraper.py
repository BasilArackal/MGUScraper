#!/usr/bin/python3
#MGUScraper 2k14 Batch 14001001-14028382
import requests
import PyPDF2
import os
import re

examCodes = ['43', '44', '45', '46', '47', '48', '49']
examCode = 0
url = "http://projects.mgu.ac.in/bTech/btechresult/index.php?module=public&attrib=result&page=result"
headers = {
	    'content-type': "multipart/form-data; boundary=---011000010111000001101001",
	    'cache-control': "no-cache"
	    }

dirs = []
prnList = []
def getPrnList():
	try:
		prnListFileName = input("\nPRNs List Filename [leave blank to scrape entire MGU]: ")
		if (prnListFileName == ''):
			prnListFileName = "t.txt"
		prnListFile = open(prnListFileName, "r")
		prnList = prnListFile.read().split("\n")
		prnListFile.close()
		try:
			print("Starting off with: PRN: "+ str( int(prnList[0]) ) )
			print(prnList)
		except ValueError:
			print("Oops! " + prnListFileName + " seem to be corrupted! :/\nPlease Try Again!")
			getPrnList()
	except FileNotFoundError:
		print("\nOops! Seems like you're missing some Files :/ \n\""+ prnListFileName +"\" not found in the current directory please try again!")
getPrnList()
try:
	for prn in prnList:
		payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"exam\"\r\n\r\n" + examCodes[examCode] +"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prn\"\r\n\r\n" + prn +"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"Submit2\"\r\n\r\nSubmit\r\n-----011000010111000001101001--"
		response = requests.request("POST", url, data=payload, headers=headers)
		if(response.text[1:4]=='PDF'):
			tempfile = open("temp.pdf", "wb")
			tempfile.write(response.content)
			tempfile.close()

			file4reading = open("temp.pdf", "rb")
			pdfText = PyPDF2.PdfFileReader(file4reading).getPage(0).extractText()
			file4reading.close()

			college = pdfText[pdfText.find("College : ")+10 :pdfText.find("Branch : ")]
			branch = pdfText[pdfText.find("Branch : ")+9 :pdfText.find("Name : ")]
			dirName = college + "/" + branch

			createDir = True
			for d in dirs:
				if(dirName == d):
					createDir = False

			if(createDir):
				os.system("mkdir -p RESULTS/" + dirName.replace(' ', '\ '))
				dirs.append(dirName)
				print("Currently working on "+ dirName)

			studentName = pdfText[pdfText.find("Name : ")+7 :pdfText.find("Register No : ")]
			filename = "RESULTS/" + college + "/" + branch + "/" + studentName + "." + prn + ".pdf"
			file = open(filename, "wb")
			file.write(response.content)
			file.close()
		else:
			print(prn + " is not a valid Register number")
	print(prnList)
	print("Done Scraping MGU")
	os.system("rm -f temp.pdf")
except KeyboardInterrupt:
	print("\n\n\nI guess that's my call! Cheers!\n\n")
	os.system("rm -f temp.pdf")