# Jack Robertson, CS5700, Project 2
# Class for segments, Proj 2 Protocol, UDP datagram

class Segment:

    def __init__(self, type, win, seq, paylen, payload):
        # segment type: DATA or ACK
        self.type = type
        # window size
        self.win = win
        # seq number, 8bit unsigned int, 0-count
        self.seqNum = seq
        # lenght of payload, n*1 Byte. DATA type = 512byte
        self.paylen = paylen
        # payload to send
        self.payload = payload

    def __str__(self):
        segment = "\n***Segment***\n|" + self.type + " | WIN size " + str(self.win) \
                  + " | Seq# " + str(self.seqNum)\
                  + " | Payload Len " + str(self.paylen) + " |\n| Payload: " + str(self.payload) + " |\n"

        return segment
