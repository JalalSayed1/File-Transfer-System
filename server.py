import socket
import sys
import common_functions as Common


def main():
    """This is the main function for the server. It creates a server socket and bind it to os kernel then initiate a queue for clients to connect then waits forever for new clients. 

    Raises:
        OSError: If a problem happened when making or binding the socket, an OSError raises.
        ConnectionResetError: If client requests to close connection, a ConnectionResetError will raise.
        UnicodeDecodeError: If Action word sent by the client was invalid, an UnicodeDecodeError will raise.
    """
    
    # Create the socket on which the server will receive new connections
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        # register the socket with the OS kernel so that messages sent to the user-defined port number are delivered to this program.
        # using "0.0.0.0" as the IP address means to bind to all available network interfaces
        # also, could have used "127.0.0.1" to bind only to the local interface
        srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
        print("[SERVER UP AND RUNNING]")
        
        # create a queue where new connection requests will be added by the OS kernel
        # This number should be small enough to not waste resources at the OS level, but also large enough so that the connections queue doesn't fill up
        srv_sock.listen(5)
        
    # handle errors:
    except OSError as OSE:
        print("OS could not initiate the socket.")
        # exit(0) means exit with no error, exit(1) means exit because of an error
        exit(1)
        
    except Exception as e: #! check for exceptions, ConnectionAbortedError, ConnectionResetError
        print(f"An unexpected error occurred.. ")
        print(e)
        # exit(0) mea
            # exit(0) means exit with no error, exit(1) means exit because of an error
        # ns xit with no error, exit(1) means exit because of an error
        exit(1)


    # Loop until errors occur:
    while True:
        
        try:
            print("Waiting for new client... ")
            
            
            # dequeue a connection request from the queue created by listen() earlier
            # if no such request is in the queue yet, this will block until one comes in
            # returns a new socket to use to communicate with the connected client plus the client-side socket's address (IP and port number):
            cli_sock, cli_addr = srv_sock.accept()

            print("Client " + str(cli_addr) + " connected.")
            
            # receive only 4 bytes for the action word ("PUT ", "GET " or "LIST")
            # NB: PUT and GET MUST have a space after the word to satisfy the requirement of 4 bytes for every ACTION word:
            data = cli_sock.recv(4)
            # .decode() could return UnicodeDecodeError:
            data_decoded = data.decode()
            
            # check what ACTION the client is requesting:
            # if ACTION is LIST, do not wait for a filename because it is not needed for this action:
            if data_decoded == "LIST":
                ACTION = "LIST"
                status = Common.send_listing(cli_sock)
            
            elif data_decoded[:3] == "PUT":
                ACTION = "PUT"
                status = Common.recv_file(cli_sock)
                
            elif data_decoded[:3] == "GET":
                ACTION = "GET"
                status = Common.send_file(cli_sock)


            # report status:
            report = f"{cli_addr}: [{ACTION} request"
            if status:
                report += f"] ACTION COMPLETED SUCCESSFULLY."
                cli_sock.sendall(report.encode())
                print(report)
            
            # if something went wrong:
            else:
                report += f"] ACTION FAILED."
                print(report)
                cli_sock.sendall(report.encode())
                raise ConnectionResetError
            
            
        # handle exceptions:        
        except ConnectionResetError as CRE:
            print(f"Client disconnected")
            # exit(0) means exit with no error, exit(1) means exit because of an error
            exit(1)
        
        except UnicodeDecodeError as UDE:
            print("Action was not a valid string.")
            # exit(0) means exit with no error, exit(1) means exit because of an error
            exit(1)
                    
        except Exception as e:
            print(f"An unexpected error occurred.. ")
            print(e)
            # exit(0) means exit with no error, exit(1) means exit because of an error
            exit(1)
        

        finally:
            
            # If an error occurs or the client closes the connection, call close socket to release the resources allocated to it by the OS:
            cli_sock.close()

    # Close the server socket as well to release its resources back to the OS
    srv_sock.close()

    # Exit with a zero value, to indicate success
    exit(0)





if __name__ == "__main__":
    main()
