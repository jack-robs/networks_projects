'''
CS5700 Project 1, Part1
Jack Robertson
File: client.py
Run with: python3 client.py
Note: do in separate terminal window from server.py
'''
from socket import *
import ipaddress


def runClient(name, port):
    '''
    Fxn: runClient()
    Does: runs a client to interact with a server.
    * run client.py in separate terminal than server.py
    Params:
    * name: str, IP address of server
    * port: int, port to bind to on server
    Returns: none
    '''
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((name, port))
    send = input("Input sentence> ")
    clientSocket.send(send.encode())
    modified = clientSocket.recv(1024)
    print("Reversed!: ", modified.decode())
    clientSocket.close()
    
    return 1




def main():
    print("welcome, this will run a TCP client, follow instructions")

    while True:

        # input and validate port
        try: 
            port = int(input("Input server port, this is likely > 1024: "))
        except ValueError:
            print("enter only numbers, no spaces, or CTR+C to quit")
            continue
        if port < 1024: 
            print("Port will throw a permission error, use port > 1024")
            continue

        # input and validae IP addr
        try: 
            addr = input("Input server IP in proper IPv4 notation: ")
            ipaddress.ip_address(addr)
            break
        except ValueError:
            print("Enter a valid IP adddress, or CTR+C to quit")
            continue

    val = runClient(addr, port)
    print("Goodbye!")

main()