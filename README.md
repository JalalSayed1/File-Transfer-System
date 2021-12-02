## About the project:

 1. It only works on a local LAN network. Therefore, it cannot transfer files to a host outside your local network.
 2. It does not have a GUI. Therefore, you need to run both client and server scripts from the command line.
 3. It only works on windows operating systems.

## How to use:

 1. Make sure you are in the right directory. If not, use `cd <YOUR/FOLDER/PATH>` to navigate to the correct folder.

2. On the command line, write the follows:
	- server.py file: `python server.py <PORT NUMBER>`
	- client.py file: `python client.py localhost <PORT NUMBER> <ACTION WORD> <FILENAME>`

**For example:**
server.py file: 

    python server.py 2000
    
client.py file: 

    python client.py localhost 2000 LIST
    python client.py localhost 2000 PUT <FILENAME>
    python client.py localhost 2000 GET <FILENAME>

## Things to consider before running it:

 1. Make sure you choose a `<PORT NUMBER>` that is in the allowed assignment port numbers range 1024 to 49151. Otherwise, the OS might not be able to bind it and it will return an error.
 2. Make sure the `<PORT NUMBER>` is consistent on the command arguments for server.py and client.py. Otherwise, client will never be able to find the server and initiate communication.
 3. When using `PUT`, make sure the file required to be uploaded to the server is in the client folder.
 4. `FILENAME` must be the full filename of the file to be uploaded/downloaded with its extension. E.g. `picture.jpg`.

## What did I learn from this:

 1. Networking and using the Socket library in Python.
 2. Developed my problem solving skills and the ability to work on a bigger project than I used to.
