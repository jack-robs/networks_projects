'''
CS5700 Project 1, Part1
Jack Robertson
File: server.py
Run with: python3 server.py
Note: do in separate terminal window from client.py
'''
from socket import *

def reverse(recMsg):
    '''
    Fxn: reverse()
    Does: reverses capitalization, and reverses order of parameter
    Param: 
    * recMsg: str, string to be reversed order/capitalization
    Returns:
    * reversed
    '''

    reversed = recMsg[::-1]

    cased = ''

    for i in reversed:
        if i.islower():
            cased += i.upper()
        else:
            cased += i.lower()

    
    return cased


def runServer(port):
    '''
    Fxn: runServer()
    Does: runs a persitent listening TCP server
    Parameters:
    * port: int, port number
    Returns: none
    '''
    
    #create, bind, and listen on socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('',port))
    serverSocket.listen(1)
    print("Server is listening!")

    #runs persistent server, will time out 
    while True:
        connectionSocket, addr = serverSocket.accept()

        #catch rec'd message from server
        recd  = connectionSocket.recv(1024).decode()
        reversedMsg = reverse(recd)
        connectionSocket.send(reversedMsg.encode())
        connectionSocket.close()





def main():

    print("Welcome, this will run a TCP server, follow instructions.")

    while True:
        try: 
            port = int(input("Input server port, recommended > 1024, ex: 12000> "))
            break
        except ValueError:
            print("enter only numbers, no spaces, or CTR+C to quit")
            continue
        if port < 1024: 
            print("Port will throw a permission error, use port > 1024")
            continue

    runServer(port)








    print("Goodbye!")

if __name__ == "__main__":
    main()
