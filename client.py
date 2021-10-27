import socket
import sys
import common_functions as Common


def main():
    """This is the main function for the client side. It makes a socket, connect to server, send Action word then get reply from server.

    Raises:
        ConnectionRefusedError: If server does not reply to the 3-way handshake, a ConnectionRefusedError will raise.
        ValueError: If argument passed in the terminal line are invalid, a ValueError will raise.
        ConnectionAbortedError: If server dropped the connection, a ConnectionAbortedError will raise.
        ConnectionResetError: If server requested to close connection, a ConnectionResetError will raise.
    """
    
    # Create the socket with which we will connect to the server:
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


    # try to connect to the server:
    try:
        print("Connecting to " + str(srv_addr) + "... ")
        
        
        # connect our socket to the server. This will actually bind our socket to a port on our side; the port number will most probably be in the ephemeral port number range and may or may not be chosen at random (depends on the OS).
        # the connect() call will initiate TCP's 3-way handshake procedure. 
        # on successful return, a TCP connection to the server will have been established:
        cli_sock.connect(srv_addr)
        
        print("Connected...")
        
    # handle errors:
    except ConnectionRefusedError as CRE:
        print(f"Server is not up or credentials provided are invalid.")
        # exit(0) means exit with no error, exit(1) means exit because of an error
        exit(1)
    
    except Exception as e:
        print(f"An unexpected error occurred.. ")
        print(e)
        # exit(0) means exit with no error, exit(1) means exit because of an error
        exit(1)

    
    # try to send and recv to and from server:
    try:
        # send what action is required from the server:
        cli_sock.sendall(ACTION.encode())
        
        if ACTION == "LIST":
            status = Common.recv_listing(cli_sock)
                
        elif ACTION == "GET ":
            status = Common.recv_file(cli_sock, FILENAME)
            
        elif ACTION == "PUT " :
            status = Common.send_file(cli_sock, FILENAME)
            
        else:
            raise ValueError
    
    
        # print a report:
        if status:
            print("Action from client side was completed successfully.")
        else:
            print("Action from client side failed.")
            
            
            
    except ValueError as VE:
        print(f"Usage: <host name or IP address> <port number> <action word> <filename>")
        # exit(0) means exit with no error, exit(1) means exit because of an error
        exit(1)
        
    except (ConnectionAbortedError, ConnectionResetError) as CE:
        print(f"The server abandoned the connection.")
        
    except Exception as e:
        print(e)


    finally:
        # If an error occurs or the client closes the connection, call close socket to release the resources allocated to it by the OS:
        cli_sock.close()

    # Exit with a zero value, to indicate success:
    exit(0)
 
 
 
 
if __name__ == "__main__":
    main()
