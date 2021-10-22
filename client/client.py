import socket
import sys
import os
import time
import traceback

#! change this before submission so it refers to a direct file: (do not remove Common)
from common_functions import common_functions as Common


def main():
    # Create the socket with which we will connect to the server
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # The server's address is a tuple, comprising the server's IP address or hostname, and port number
    srv_addr = (sys.argv[1], int(sys.argv[2]))
    
    ACTION = str(sys.argv[3])
    if ACTION in ["PUT", "GET"]:
        # we only have filename argument if action is put or get:
        FILENAME = str(sys.argv[4])
        # server will be expecting 4 bytes of data as ACTION word so if ACTION is PUT or GET, we need to add b' ' to make it 4 bytes
        ACTION = ACTION + ' '
        print(f"action word is now: {ACTION} with len = {len(ACTION)}")

    """ 
    Enclose the connect() call in a try-except block to catch
    exceptions related to invalid/missing command-line arguments, 
    port number out of range, etc. Ideally, these errors should 
    have been handled separately.
    """
    # try to connect to server:
    try:
        print("Connecting to " + str(srv_addr) + "... ")
        
        """
        Connect our socket to the server. This will actually bind our socket to
        a port on our side; the port number will most probably be in the
        ephemeral port number range and may or may not be chosen at random
        (depends on the OS). The connect() call will initiate TCP's 3-way
        handshake procedure. On successful return, said procedure will have
        finished successfully, and a TCP connection to the server will have been
        established.
        """
        cli_sock.connect(srv_addr)
        
        print("Connected...")
        
    # handle errors:
    except Exception as e: #! add exceptions
        # Print the exception message
        print(e)
        print(traceback.format_exc())
        # Exit with a non-zero value, to indicate an error condition
        exit(1)

    """
    Surround the following code in a try-except block to account for
    socket errors as well as errors related to user input. Ideally
    these error conditions should be handled separately.
    """
    # try to send and recv to and from server:
    try:
        # send what action is required from the server:
        cli_sock.sendall(ACTION.encode())
        # time.sleep(0.1)
        
        # if action is get or put, send "START_FILENAME" + filename + "END_FILENAME"
        # if action is put, send the file data
        # if action is get, wait for response:
        if ACTION == "LIST":
            print(f"Action is {ACTION}")
            status = Common.recv_listing(cli_sock)
                
        elif ACTION == "GET ":
            print(f"Action is {ACTION}")
            # cli_sock.send("START_FILENAME".encode())
            # cli_sock.sendall(FILENAME.encode())
            # cli_sock.send("END_FILENAME".encode())
            status = Common.recv_file(cli_sock, FILENAME)
            
        elif ACTION == "PUT " :
            print(f"Action is {ACTION}")
            # cli_sock.sendall("START_FILENAME".encode())
            # cli_sock.sendall(FILENAME.encode())
            # cli_sock.sendall("END_FILENAME".encode())
            status = Common.send_file(cli_sock, FILENAME)
            
        else:
            print(f"Action is not known")
            raise ValueError
        

        # get a report from server then print it:
        print(f"Waiting for a response from server..")
        respond = cli_sock.recv(4096)
        print(f"{srv_addr}: {respond.decode()}")
        
        # report about client status:
        print("Action from client side ", end="")
        if status:
            print("was completed successfully.")
        else:
            print("failed.")
        
        
        # report what happened:
        # print(f"{srv_addr}: [{ACTION} request", end="")
        # # if status is true and action is put or get, add FILENAME to the report:
        # if status and ACTION in ["PUT", "GET"]:
        #     print(f" {FILENAME}] ACTION COMPLETED SUCCESSFULLY.")

        # # if status is true and action is list, complete the report normally:
        # elif status:
        #     print(f"] ACTION COMPLETED SUCCESSFULLY.")
        
        # # if something wrong happend:
        # else:
        #     print(f"] ACTION FAILED.")
        

        
        
        #! for sending listing example:
        #!send_listing = Common.send_listing(cli_sock)
        #!if send_listing:
        #!    print("Listing sent successfully")
        
        #! for sending file example:
        # Loop until either the server closes the connection or the user requests termination
        #!bytes_sent = Common.send_file(cli_sock, "win11.iso") #! need to change filename to argv[]
        # Common.send_file(cli_sock, 0) # indicating end of transmission
        
        #!print(f"the byte len is: {bytes_sent}", flush=True)
        #!if bytes_sent == 0: # keyboard_to_socket will return 0 if it found that we wrote "EXIT\n"
        #!    print("Send complete.")
            # break

            # Then, read data from server and print on screen
            # bytes_read = socket_to_screen(cli_sock, srv_addr_str)
            # if bytes_read == 0:
            # 	print("Server closed connection.")
            # 	break
            
    except ValueError as VE:
        print(f"Error: It is most likely that you passed a wrong argument.")
        print(VE)

    finally:
        """
        If an error occurs or the server closes the connection, call close() on the
        connected socket to release the resources allocated to it by the OS.
        """
        cli_sock.close()

    # Exit with a zero value, to indicate success
    exit(0)
 
 
 
 
if __name__ == "__main__":
    main()
