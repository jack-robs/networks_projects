import sys
import socket

from ServerWorker import ServerWorker
"""
Purpose: 

Launches the server application for an inputted server port. 

NOTE: THIS CODE SECTION WAS PROVIDED BY KUROSE LAB6
"""
class ServerLauncher: 
    
    def main(self):

        try:
            #SERVER_PORT = int(sys.argv[1])
            SERVER_HOSTNAME = 'localhost'
            SERVER_PORT = 8000
        except:
            print("[Usage: Server.py Server_port]\n")
		
        rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rtspSocket.bind((SERVER_HOSTNAME, SERVER_PORT))
        rtspSocket.listen(5)        
        print('Server is listening...')
		# Receive client info (address,port) through RTSP/TCP session
        while True:
            # create a dictionary to store client information. 
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            
            # TODO: implement the Server worker class. 
            ServerWorker(clientInfo).run()		

if __name__ == "__main__":
    (ServerLauncher()).main()


