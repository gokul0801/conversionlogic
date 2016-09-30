import optparse
import datetime

### Process input Events file
### Store the event information for each entry in the deviceId dictionary
### Sort the list of events for each device based on timestamp
def process_file(opts):
    f = file(opts.inputFile)
    deviceIdDict = {}
    userDict = {}
    for line in f:
	    arr = line.strip().split(',')
	    timestamp = datetime.datetime.strptime(arr[0], '%Y-%m-%d %H:%M:%S')
	    deviceId = arr[1]
	    event = {
	   	   'timestamp' : timestamp,	
           	   'username' : arr[2],
           	   'channel' : arr[3],
	   	   'action' : arr[4],
	   	   }
	    deviceIdDict.setdefault(deviceId, []).append(event)
    f.close()

    ### Construct the userevent dictionary based on events for users across devices
    ### Sort the event lists from different devices of the same user to get timeordered list of events
    userEventDict = {}
    for device in deviceIdDict:
        username = None
	for event in deviceIdDict[device]:
            if username is None and event['username'] != '':
	       username = event['username']
	       break	
        if username is not None:
	   for event in deviceIdDict[device]:
		userEventDict.setdefault(username, []).append(event)

    for username in userEventDict:
        eventLst = sorted(userEventDict[username], key=lambda k: k['timestamp'])
        channels = ''
        for event in eventLst[:-1]:
	    channels += event['channel'] + ','
        channels += eventLst[-1]['channel']
	userDict[username] = channels
    for user, channels in userDict.items():
        print user + ': ' + channels
        



if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action='store', dest='inputFile', metavar='FILE', help="input events file")
    opts, args = parser.parse_args()
    if opts.inputFile is None:
       raise Exception("Error: Input file not given")
    process_file(opts)


