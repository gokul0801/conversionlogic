import optparse
import datetime

### Process input Events file
### Store the event information for each entry in the deviceId dictionary
### Sort the list of events for each device based on timestamp
### Print the channel list for each device
def process_file(opts):
    f = file(opts.inputFile)
    deviceIdDict = {}
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
    for device in deviceIdDict:
 	output = device + ': '
        eventLst = sorted(deviceIdDict[device], key=lambda k: k['timestamp'])
        for event in eventLst[:-1]:
	    output += event['channel'] + ','
	output += eventLst[-1]['channel']
	print output


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action='store', dest='inputFile', metavar='FILE', help="input events file")
    opts, args = parser.parse_args()
    if opts.inputFile is None:
       raise Exception("Error: Input file not given")
    process_file(opts)


