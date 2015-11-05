import optparse
import datetime

### Process input Events file
### Store the event information for each entry in the deviceId dictionary
### Sort the list of events for each device based on timestamp
def process_file(opts):
    f = file(opts.inputFile)
    deviceIdDict = {}
    freqDict = {}
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
    ### Construct the frequency dictionary based on common channel paths for devices
    for device in deviceIdDict:
        channels = ''
        eventLst = sorted(deviceIdDict[device], key=lambda k: k['timestamp'])
        for event in eventLst[:-1]:
	    channels += event['channel'] + ','
	channels += eventLst[-1]['channel']
        freqDict[channels] = freqDict.get(channels, 0) + 1
    ### Print the sorted output based on values for frequencny dicitonary 
    for channels, freq in sorted(freqDict.iteritems(), key=lambda k: k[1], reverse=True):
        print str(freq) + ': ' + channels
            



if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', dest='inputFile', metavar='FILE', help="input events file")
    opts, args = parser.parse_args()
    if opts.inputFile is None:
       raise Exception("Error: Input file not given")
    process_file(opts)


