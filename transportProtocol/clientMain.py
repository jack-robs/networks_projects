# Jack Robertson Proj 2, CS5700
# main() for Proj2 client
import pickle
import segmentClass as segment
from socket import *
import sys
import os
import ipaddress

def checkLength(payloadBuff, payloadLen):
    '''
    fxn: checkLength()
    does: confirms payload length of buffer storing a payload being built is
    less than the max payload length
    params:
    - payloadBuff: list, strings, i.e. ['a', 'b', ...]
    - payloadLen: int, max payload, bytes, i.e. 512
    returns: boolean, t/f buff < payloadmax
    '''

    payload = "".join(payloadBuff)
    byteLength = len(payload.encode('utf-8'))

    return byteLength < payloadLen

def generatePayloads(filename):
    '''
    fxn: generatePayloads()
    does: generates a list[] of payloads read-in from file
    - each index in the list is a payload
    - each payload is < max paylaod length allowed
    params:
    - filename: str, filename in OS to read payload in from
    returns: payloads, a list of payloads
    '''


    payloads = []
    rawIn = ''

    # read in file into single string
    with open(filename) as f:
        for i in f:
            rawIn += i

    # build temp payload storage. once buffer >= max payload, add to final paylaods[]
    buildPayloadBuffer = []
    for char in rawIn:
        # check if max payload size hit yet
        if not checkLength(buildPayloadBuffer, 512):
            addPayload = buildPayloadBuffer[:-1]
            payload = ''.join(addPayload)
            payloads.append(payload)
            del buildPayloadBuffer[:]

        #if end of payload from filename found, build final payload
        if char == '\n':
            payload = ''.join(buildPayloadBuffer)
            payloads.append(payload)
            break
        buildPayloadBuffer.append(char)

    return payloads


def buildSegs(packets):
    '''
    fxn: buildSegs()
    does: buiilds a list[] of segments that are Segment Objects
    - have payload set
    - have length of payload set
    - have type set
    - do not have seq num or window size set
    params:
    - packets: list[] of strings, each index = a packet's payload
    returns:
    - segBUffer: list[] of segment objects
    '''

    segBuffer = []

    for i in range(len(packets)):
        type = 'DATA'
        win = None
        sedNum = None
        payLen = len(packets[i].encode('utf-8'))
        payLoad = packets[i]
        seg = segment.Segment(type, win, sedNum, payLen, payLoad)
        segBuffer.append(seg)

    return segBuffer

def runGBN(segList, destIP, destPort, window):
    '''
    fxn: runGBN()
    does: sends segments/packets from the segList per the rules of TCP-GBN
    params:
    - segList: list[] of segment objects to send to server. all the contents of the 
    input file are packetized across this list of segments' payloads
    - destIP: str, server's IP
    - destPort: int, server's port
    - window: int window size, 
    '''

    complete = True

    # set initial values per Kurose p 223
    base = 1
    nextSeqNum = 1
    nextPacket = 0
    segsLeft = len(segList)

    while segsLeft > 0:

        '''
        kurose 223: `rdt_send(data) from GBN FSM
        '''
        # send packet or window violation
        if (nextSeqNum < (base + window)):
            segment = segList[nextPacket]
            segment.seqNum = nextSeqNum
            sock = socket(AF_INET, SOCK_DGRAM)
            dgram = pickle.dumps(segment)
            sock.sendto(dgram, (destIP, destPort))
            print("\nSending and advancing sequence number:\n", segment)
            nextSeqNum += 1
            nextPacket += 1

            # TODO why do this...
            if base == nextSeqNum:
                # start timer
                print("\nStart timer\n")
                sock.settimeout(10)
        else:
            # do nothing - send no packets, need window space to open up
            pass

        
        '''
        kurose 223: `timeout` from GBN FSM
        '''
        # check for timeout condition
        curr = sock.gettimeout()
        if curr == None:
            pass
        elif curr < 10:
            pass
        else:
            print("\ntimeout hit\n")
            sock.settimeout(10)
            for i in range(base, nextSeqNum):
                segment = segList[i]
                segment.seqNum = i
        


        '''
        kurose 223: `rdt_rcv(rcvpkt) && notcorrupt(rcvpkt)` from GBN FSM
        '''
        try:
            ack, serverAdr = sock.recvfrom(2048)
            ackSeg = pickle.loads(ack)
            print("recv from server:", ackSeg)
            base = ackSeg.seqNum + 1
            segsLeft -= 1
            if base == nextSeqNum:
                sock.settimeout(None)
            else:
                sock.settimeout(10)
        except:
            sock.settimeout(10)


    # all packets from segmenet list sent
    return complete

def main():

    #sender destIP, destPort, window_size, inputfil

    args = sys.argv
    if len(args) == 1:
        print("proper input: python3.6 clientMain.py <destination ip> <destination port> <window size> <inputfile.txt")
        exit()
    try:
        destIP = args[1]
        destPort = int(args[2])
        window = int(args[3])
        inputFile = args[4]
    except IndexError:
        print("proper input: python3.6 clientMain.py <destination ip> <destination port> <window size> <inputfile.txt")
        exit()

    try:
        ipaddress.ip_address(destIP)
    except ValueError:
        print("please input proper format IPv4")
        exit()

    if not os.path.exists(inputFile):
        print("input file not found, exiting")
        exit()



    # read file into payloads
    payloads = generatePayloads(inputFile)

    # build segments from playoads, w/o sequence number or window size values
    segments = buildSegs(payloads)

    # run GBN. This is 'call from above'
    send = runGBN(segments, destIP, destPort, window)

    # end of session reporting
    if send:
        print("Successful session, goodbye")
        exit()
    else:
        # TODO better error handling T/E block for `send` result
        print("unknown failures to session, goodbye")
        exit()


main()
