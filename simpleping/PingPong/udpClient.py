'''
Part 3, Project 1, CS5700
Jack Robertson
file: udpClient.py
UDP Client
'''
from socket import *
import ipaddress
import time


def runPing(hostname, port):
    '''
    Fxn: runClient()
    Does: runs UDP pinger client
    Params:
    * hostname: str, IPv4 addr
    * port: int, port
    Returns: int, 1
    '''

    # run pinger
    report = {'PONG':[], 'timeouts':0}
    count = 0
    while count < 10:
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.settimeout(4)
        message = 'ping'
        clientSocket.sendto(message.encode(), (hostname, port))
        print("Sending...")

        try: 
        # can hang her, set timeout value for 4 sec... how?
            pong, serverAdr = clientSocket.recvfrom(2048)
        except timeout:
            print("Timeout")
            report['timeouts'] += 1
            count += 1
            continue

        msg = pong.decode()
        print("Rec'd:", msg, 'from: ', serverAdr)
        report['PONG'].append(serverAdr)
        clientSocket.close()
        count += 1


    return report

def main():

    addr = '127.0.0.1'
    port = 1025

    results = runPing(addr, port)
    pongs = len(results['PONG'])
    fails = results['timeouts']
    print("\n\n*******UDP PING TEST RESULTS*******")
    print(f"Successful Pings to {addr} at port {port}:", pongs)
    print("Timeouts:", fails)
    print("Success Rate:", str(pongs/(fails+pongs)*100) + "%")
    print("Fail Rate:", str(fails/(fails+pongs)*100) + "%")
    print("\n\nFull report:", results, "\n\n")
    print("Goodbye!")


main()
