import socket
import sys
import common_functions as Common # I have made a super link for this file to the client file
import traceback

# def deal_with_put(socket, data):
    
#     try:
#         # filename will be in between START_FILENAME and END_FILENAME (client must send it in this format):
#         START_FILENAME, END_FILENAME = "START_FILENAME", "END_FILENAME"
#         # got_filename to be used in the if statements to check if we received full filename or not yet
#         got_filename = False

#         # data = bytearray(1)
#         while len(data) > 0:
            
#             data = socket.recv(4096)
            
#             # NB: max filename in windows is 255-260 characters, 255 characters in MacOS but 255 "bytes" in Linux.
#             # store the filename which will be just after START_FILENAME:
#             if START_FILENAME.encode() in data:
#                 data_decoded = data.decode()
#                 # get the index of the first charecter of the filename:
#                 start_index = data_decoded.index(START_FILENAME) + len(START_FILENAME)
                
#                 # filename is from start_index to the end of the data stream
#                 # we could have a short filename which will be sent in a single send() request or a long filename which will be sent via multiple send() requests
#                 # we will be checking on this very shortly
#                 FILENAME = data_decoded[start_index:]
                
#                 # if filename is short, END_FILENAME will be present in the same data stream:
#                 if END_FILENAME.encode() in data:
#                     # strip it out from the FILENAME:
#                     FILENAME = FILENAME[:len(END_FILENAME)]
#                     # strip out the FILENAME and END_FILENAME from data so we can use it later for writing the file:
#                     end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
#                     # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345":
#                     data = data[end_index:]
                    
                    
#                     #? do the writing file process (loop until writing is done)
                    
                
#                 # if filename is too long
#                 # this block will run if END_FILENAME is not present in data and we have not got the full filename yet:
#                 elif (END_FILENAME not in data_decoded) and (not got_filename):
#                     # in case the filename is too long, it will be sent on multiple send requests so we need a while loop to store the filename after each recv call:
#                     FILENAME += data_decoded
                    
#                     # loop until END_FILENAME is received:
#                     while END_FILENAME.encode() not in data:
#                         data = socket.recv(4096)
#                         data_decoded = data.decode()
#                         FILENAME += data_decoded
                        
#                         # if END_FILENAME in data_decoded:
#                         #     # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
#                         #     FILENAME = FILENAME[:len(END_FILENAME)]
                    
#                     # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
#                     FILENAME = FILENAME[:len(END_FILENAME)]
#                     # strip out the FILENAME + END_FILENAME from data so we can use it later for writing the file:
#                     end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
#                     # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345":
#                     data = data[end_index:]
                    
                    
#                     #? do the writing file process (loop until writing is done)
            
            
            
            
    
    
#     except OSError as OSE: #! add other exceptions
#         print(f"Filename is too long and cannot be created in {sys.platform} OS. {OSE}")
#         # return false indicating error occurred:
#         return False

#     # if all were fine, return true indicating success:
#     else:
#         return True

#* ------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    # Create the socket on which the server will receive new connections
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ 
    Enclose the following two lines in a try-except block to catch
    exceptions related to already bound ports, invalid/missing
    command-line arguments, port number out of range, etc. Ideally,
    these errors should have been handled separately.
    """
    try:
        """
        Register the socket with the OS kernel so that messages sent
        to the user-defined port number are delivered to this program.
        Using "0.0.0.0" as the IP address so as to bind to all available
        network interfaces. Alternatively, could have used "127.0.0.1"
        to bind only to the local (loopback) interface, or any other IP
        address on an interface of the computer where this program is
        running (use "ipconfig /all" to list all interfaces and their IP
        addresses).
        """
        srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
        print("[SERVER UP AND RUNNING]")
        """
        Create a queue where new connection requests will be added by
        the OS kernel. This number should be small enough to not waste
        resources at the OS level, but also large enough so that the
        connections queue doesn't fill up. For this latter, one should
        ideally have an idea of how long it takes to serve a request
        and how frequently clients initiate new connections to the
        server.
        """
        srv_sock.listen(5)
        
    # handle errors:
    except Exception as e: #! check for exceptions
        # Print the exception message
        print(e)
        # Exit with a non-zero value, to indicate an error condition.
        # exit(0) means exit with no error, exit(1) means exit because of an error
        exit(1)

    # Loop forever (or at least for as long as no fatal errors occur)
    while True:
        """
        Surround the following code in a try-except block to account for
        socket errors as well as errors related to user input. Ideally
        these error conditions should be handled separately.
        """
        try:
            print("Waiting for new client... ")
            
            """
            Dequeue a connection request from the queue created by listen() earlier.
            If no such request is in the queue yet, this will block until one comes
            in. Returns a new socket to use to communicate with the connected client
            plus the client-side socket's address (IP and port number).
            """
            cli_sock, cli_addr = srv_sock.accept()

            print("Client " + str(cli_addr) + " connected.")

            # Loop until either the client closes the connection or the user requests termination
            # while True:
            
            # receive only 4 bytes for the action word ("PUT ", "GET " or "LIST")
            # NB: PUT and GET MUST have a space after the word to satisfy the requirement of 4 bytes ACTION word must be received at the first instance:
            data = cli_sock.recv(4)
            data_decoded = data.decode()
            
            # check what ACTION the client is requesting:
            # if ACTION is LIST, do not wait for a filename because it is not needed for this action:
            if data_decoded.startswith("LIST"):
                ACTION = "LIST"
                print(f"Action required is {ACTION}")
                status = Common.send_listing(cli_sock)
            
            elif data_decoded[:3] == "PUT":
                ACTION = "PUT"
                print(f"Action required is {ACTION}")
                status = Common.recv_file(cli_sock)
                
            elif data_decoded[:3] == "GET":
                ACTION = "GET"
                print(f"Action required is {ACTION}")
                print(f"running send_file now..")
                status = Common.send_file(cli_sock) #! need to make send_file like recv_file, to get the filename from data stream
                print(f"status from send_file is {status}")
            # elif ACTION:=data_decoded[:3] in ["GET", "PUT"]:
            #     # store what we have got after the ACTION word in data as the FILENAME
            #     FILENAME = data_decoded[3:]
                
            #     # in case the filename is too long, it will be sent on multiple send requests so we need a while loop to store the filename after each recv:
            #     data = bytearray(1)
            #     while len(data) > 0:
            #         # keep recv if filename is too long:
            #         data = cli_sock.recv(4096)
            #         data_decoded = data.decode()
            #         # add the data we just received to the FILENAME:
            #         FILENAME += data_decoded

            #     if ACTION == "GET":
            #         status = Common.send_file(cli_sock, FILENAME)
                    
            #     elif ACTION == "PUT":
            #         status = Common.recv_file(cli_sock, FILENAME)

                
                
            # if ACTION word is not identified:
            else: #! maybe add an wrong args passed exception
                message = "Server could not identify what action is required."
                # print message in server screen:
                print(message)
                # then send it to client
                cli_sock.sendall(message)
                
                
                
            
            # report what happened:
            report = f"{cli_addr}: [{ACTION} request"
            # if status is true and action is put or get, add FILENAME to the report:
            if status and ACTION in ["PUT", "GET"]:
                report += f"] ACTION COMPLETED SUCCESSFULLY." #!try adding {FILENAME}

                # now, print the report in server's screen and send it to client:
                cli_sock.sendall(report.encode())
                print(report)
                

            # if status is true and action is list, complete the report normally:
            elif status:
                report += f"] ACTION COMPLETED SUCCESSFULLY."

                # now, print the report in server's screen and send it to client:
                cli_sock.sendall(report.encode())
                print(report)
            
            # if something went wrong:
            else:
                report += f"] ACTION FAILED."
                print(report)
                raise ConnectionResetError
            
            
            
            
            
                
                
                
                
                
                
                
                
                
                #! for recv listing example:
                #!recv_listing = Common.recv_listing(cli_sock)
                #!print(recv_listing, flush=True)
                #!if recv_listing:
                #!    break
                
                
                #! for recv data example:
                # First, read data from client and print on screen
                #!bytes_read = Common.recv_file(cli_sock, "win11.iso")
                # just to not print the last byte before terminating the connection, which will always be 0:
                #!if bytes_read != 0:
                #!    print(f"Bytes read: {Common.calculate_bytes(bytes_read)}")
                #!    print()
                #!elif bytes_read == 0:
                #!    break
                    # print("Client closed connection.")
                    
        except ConnectionResetError as CRE:
            print(f"Client closed connection")
            print(CRE)
            
        # except ValueError as VE:
        #     print(f"Usage: <host name or IP address> <port number> <action word> <filename>")
        #     print(VE)
                    
        except Exception as e:
            print(e)
            print(traceback.format_exc())
        

        finally:
            """
            If an error occurs or the client closes the connection, call close() on the
            connected socket to release the resources allocated to it by the OS.
            """
            cli_sock.close()

    # Close the server socket as well to release its resources back to the OS
    srv_sock.close()

    # Exit with a zero value, to indicate success
    exit(0)





if __name__ == "__main__":
    main()
