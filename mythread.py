import threading
import time
import json

def writeDataToLog():
	json_data=open("last.json").read()
	data = json.loads(json_data)
	json_data2=open("log.json").read()
	data2 = json.loads(json_data2)
	data2['log'].append(data)
	with open('log.json', 'w') as outfile:
 		json.dump(data2, outfile)

class checkWeight():

    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
	thread.start()
    def run(self):
	curentData = {"Weight":0}
        while True: 
		try :    
			json_data=open("last.json").read()
			data = json.loads(json_data)
			if data['Weight'] != curentData['Weight'] :
				writeDataToLog()
				curentData = data
				print "changed"
		except:
			print "Load Problem"  
