from socket import *
import pickle
import segmentClass as segment
import sys
import os

def runGBN(listenPort, window_size, outputFile):
    '''
    fxn: runGBN()
    does: runs a server implementing a version of TCP(GBN) for reliable data transfer
    params:
    - listenPort: int, port, must be > 1025
    - window_size: int, size of window, must be > 0
    - outputFile: str, file that payload is saved to 
    returns: none
    '''


    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', listenPort))
    print("\nserver running, 10 second timeout with no connection received\nProgram exit on 3 consecutive timeouts")
    print("\nAfter initial connection, client must wait until notification that server is ready for new connection")
    recvSegs = []

    if not os.path.exists(outputFile):
        with open(outputFile, 'w') as f:
            pass

    expectedSeq = 1
    timeouts = 0

    while True:
        serverSocket.settimeout(10)
        try:
            message, address = serverSocket.recvfrom(1025)
            recvsegment = pickle.loads(message)
            if recvsegment.seqNum != expectedSeq:
                print("Unexpected seq #, sent:", recvsegment.seqNum, 'expected', expectedSeq)
                continue
            else:
                print(f"\nServer received, processing reply, saving payload to {outputFile}...\n")
                timeouts = 0

                # save payload
                with open(outputFile, 'a') as f:
                    f.write(recvsegment.payload)

                # make packet
                type = 'ACK'
                win = None
                # will resend back old seq# if `if` is hit in prior loop
                seq = expectedSeq
                payload = ''
                payloadLen = len(payload.encode('utf-8'))
                serverSeg = segment.Segment(type, win, seq, payloadLen, payload)
                dgram = pickle.dumps(serverSeg)
                serverSocket.sendto(dgram, address)
                print('server sent')
                expectedSeq += 1
                serverSocket.settimeout(None)
                serverSocket.settimeout(10)
        except timeout:
            if timeouts < 3:
                print("\nReady for new connections...\n")
                serverSocket.settimeout(None)
                serverSocket.settimeout(10)
                expectedSeq = 1
                timeouts += 1
                continue
            else:
                print("\n3 timeouts, no connection received, exiting server")
                exit()

def main():

        # python3.6 server.py <listening port> <window_size> <output_file>
        args = sys.argv
        if len(args) == 1:
            print("proper input: python3.6 serverMain.py <listen_port> <window_size> <outputfie.txt>")
            exit()
        if int(args[1]) < 1026:
            print("port must be > 1026")
            exit()
        if int(args[2]) < 2:
            print("window size must be > 1")
            exit()

        try:
            listenport = int(args[1])
            window_size = args[2]
            outputFile = args[3]
        except IndexError:
            print("proper input: python3.6 serverMain.py <listen_port> <window_size> <outputfie.txt>")
            exit()

        runGBN(listenport, window_size, outputFile)



main()
