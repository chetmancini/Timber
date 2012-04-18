##############################################################################
#                                                                            #
#  .___________. __  .___  ___. .______    _______ .______                   #
#  |           ||  | |   \/   | |   _  \  |   ____||   _  \                  #
#  `---|  |----`|  | |  \  /  | |  |_)  | |  |__   |  |_)  |                 #
#      |  |     |  | |  |\/|  | |   _  <  |   __|  |      /                  #
#      |  |     |  | |  |  |  | |  |_)  | |  |____ |  |\  \----.             #
#      |__|     |__| |__|  |__| |______/  |_______|| _| `._____|             #
#                                                                            #
#----------------------------------------------------------------------------#
# request_generator.py                                                       #
##############################################################################

### Imports ##################################################################
import httplib, urllib
import multiprocessing
import threading

### Parameters ###############################################################
IPADDRESS = "127.0.0.1"
PORT = 80
TIMEOUT = 10
COUNT = 100000
NUM_PROCESS = 10

### Fuctions #################################################################
def executeRequest(connection):
	params = {'@number': 12524, '@type': 'issue', '@action': 'show'}
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	connection.request("POST", "", urllib.urlencode(params), headers)
	response = connection.getresponse()
	print "Status",response.status,"Reason" response.reason, "Data",response.read()

def createConnection():
	return httplib.HTTPConnection(IPADDRESS, PORT, timeout=TIMEOUT)

def threadExecute():
	with createConnection() as connection:
		connection = createConnection()
		for i in range(COUNT):
			executeRequest(connection)
		connection.close()

### Main #####################################################################
if __name__ == "__main__":
	"""
	Main function to run
	"""
	pool = multiprocessing.Pool(None)
	threads = []

	for i in range(NUM_PROCESS):
		nextthread = threading.Thread(None, threadExecute, "thread"+str(i), (), {})
		threads.append(nextthread)
		nextthread.start()

