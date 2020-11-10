import sys
import socket

# Author(s): Zak Hussain, Cat Smith
"""
Purpose: 
 
The ClientLauncher class is used to launch a client application process. 
It does the following: 
1. Reads in user input: 
    * address of server 
    * rtsp port number
    * rtp port number
    * name of filepath for media content to stream
2. It creates a Tkinter obj to pass to the client app, which allows the client 
   to send control packets to the streaming server. 
"""


#=========================== Original Class ++++++++++++++++++++++++++
# class ClientLauncher: 

#     def main(self):

#         print("Client application is Launching")
#         def __init__(self, master, serveraddr, serverport, rtpport, filename):
#             try:
#                 master = sys.argv[1]
#                 serveraddr = int (sys.argv[2])
#                 serverport = int (sys.argv[3])
#                 rtpport = sys.argv[4]
#                 filename = sys.argv[5]

#             except IndexError:
#                 print("The following arguments are required: [master, serveraddr, serverport, rtpport, filename].")
#                 sys.exit(1)

#             # Create client based on user arguments.
#             client = ClientWorker(master, serveraddr, serverport, rtpport, filename)

#             # Initiate contact with server.
#             client.connectToServer()
#             client.sendRtspReq(0)

#             # Initiate GUI
#             client.createWidgets()

# ======================================================== temp class
from tkinter import Tk
from ClientWorker import ClientWorker
class ClientLauncher: 

    def main(self):

        print("Client application is launching")

        serverAddr = '127.0.0.1'
        serverPort = 8000
        rtpPort = '1025'
        fileName = "./movie.Mjpeg"  
        
        root = Tk()
        
        # Create a new client
        app = ClientWorker(root, serverAddr, serverPort, rtpPort, fileName)

        app.master.title("RTPClient")   
        root.mainloop()

if __name__== "__main__": 
    (ClientLauncher()).main()