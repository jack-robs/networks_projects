# Project 2: Transport Protocol (GBN implementation)
## Jack Robertson
## CS5700, 13JUN2020
---

## Files Overview:

```
$ transportProtocol
├── binfile.txt
├── clientMain.py
├── output.txt
├── segmentClass.py
├── serverMain.py
```

- binfile.txt: binary file mock, single string of AAAABBB......ZZZ1111222, etc..
- output.txt: example of output file from running server code and saving its received payloads to a file.
- clientMain.py: client code, implements a version of Go-Back-N for reliable data transfer, server-side
- serverMain.py: server code, implements a version of Go-Back-N for reliable data transfer, server-side
- segmentClass.py: class for packet/segment objects, used to implement packet abstraction. Both server/client use it via imports


## Running the code:

**First: run server*:*
- terminal 2: `python3.6 serverMain.py <listen port> <window_size> <outputfile.txt>`
    - example: `python3.6 serverMain.py 1026 4 myoutput.txt`

- server behavior:
    - initial information:
        - prompt to show server is running
        - explain server exits after 3 consecutive timeout periods (timeout = 10s) AND no connection received. 
        - explain client must wait for `Ready for new connections` prompt prior to re-runnning client
    - send/received behavior:
        - implements GBN
        - outputs prompt when connection is received
        - outputs prompt when payload ACK is sent back
    - close server:
        - auto-closes w/ `exit()` when 3 consecutive timeouts occur w/ no connection. Utilizes `socket.timeout()` plus timeout count tracker


**Second: run client**
- terminal 1: `python3 clientMain.py <destination ip> <destination port> <window size> <inputfile.txt>`
    - example: `python3.6 clientMain.py 127.0.0.1 1026 4 binfile.txt`
    - note: binfile.txt must already exist

- client behavior: 
    - send/receive behavior:
        - Implements GBN
        - outputs sent notification
        - outputs sent segments, outputs ACK segments recevied from server
        - outputs closing prompt when all segments are sent and ACKs received


## Key points:

**admin**
- are my functions documented and code commmented: yes
- error handling, does it occur: yes. try/except blocks, command line input is validated for logical safety, timeouts are employed
- what protocol did I use: GBN, not SR

**client**
- command line input is read-in by `sys.argv`
- input file that contains payload data must exist for client in same directory, error handling exists for this.
- `generatePayloads(inputFile)` creates `list[]` of payload strings that are < 512 bytes long
- `buildSegs(payloads)` creates a list of objects that have `obj.payload` set to the payloads `generatePayloads()`. These are my 'segments', they have no seq num/window size yet though
- sending objects over sockets: uses python's `pickle` library
- `runGBN(segments, destIp, destPort, window)` runs the transport protocol. Objects are sent as segments via `sockets` use,  sequence numbers setting and resends occur per GBN 
- Does NOT handle corrupt packets, assumed to be not-corrupted per prompt from textbook

**server**
- command line input is read-in by `sys.argv`
- the output file is created in the same directory, if it doesn't already exist.
- `runGBN(listenPort, window_size, outputFile)` implements GBN protocol on the server-side
- `outputFile.txt` is appended to w/ each packet that is received
- server sends an ACK packet built from the segmentClass.py file.
- Does NOT handle corrupt packets, assumed to be not-corrupted per prompt from textbook

**Further improvements**
- better tests to confirm various traits of GBN
- keep client live, create option to re-send
- this really seems to be a usecase for `fork()` or `thread()` to handle multiple connections
- checksum implementation for corrupt packets





































