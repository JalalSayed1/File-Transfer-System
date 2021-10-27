import time
import os
from os import listdir
from os.path import isfile, join


def send_file(socket, FILENAME=""):
    """Send a file over the socket provided.
    If the server is sending the file: firstly, receive the filename then start sending the file to client.
    If the client is sending the file: check that the filename provided exists in client folder then send the file.

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.
        FILENAME (str, optional): The filename to be sent over the socket. If server is the one sending, leave it as default value. Defaults to "".

    Raises:
        FileNotFoundError: If client is sending and filename provided does not exist in client folder, FileNotFoundError will raise.

    Returns:
        boolean: True indicates success and False indicates a problem.
    """

    # get current time. This is just for fun to calculate how long the code will take to execute:
    start_time = time.time()

    # this is the byte that will indicate the end of the filename and transmission:
    END_FILENAME, END_TRANSMISSION = "|", "|"

    try:
        
        # if FILENAME is not specified, that mean the server is the one sending and client is receiving
        # this means the client must send the FILENAME just before sending the data so we will capture it by recv_filename():
        if FILENAME == "":
            # this var is for error reporting and wait_for_response()
            client_sending = False
            
            # recv_filename will return the filename and any extra data was received with the filename data stream
            # however, if client wants to GET this file, that means he will not send any extra data after the filename
            # so we will not use it:
            FILENAME, _ = recv_filename(socket, END_FILENAME)

            
            
        # if FILENAME is specified, that means the server is receiving and client is sending:
        else:
            # this var is for error reporting and wait_for_response()
            client_sending = True
            
            # first thing, check that the filename provided exists:
            filenames = get_filenames()
            if FILENAME not in filenames:
                raise FileNotFoundError
            
            # "|" indicates end of filename
            to_send = FILENAME + END_FILENAME
            socket.sendall(to_send.encode())
            
            

        # open the required filename in read binary mode:
        with open(FILENAME, 'rb') as f:
            # because I used for loop here, sendall() will not make recv() get b'' when communication is done. NB: b'' indicates end of transmission
            # so I sent "|" to solve this problem:
            for data in f:
                socket.sendall(data)


        # send "|" indicating end of transmission:
        socket.sendall(END_TRANSMISSION.encode())
        
        
        # print how long sending the file took:
        finish_time = time.time()
        difference = finish_time - start_time
        print(flush=True) # just a blank line
        # print the time taken to execute the function in a nicely formatted way:
        # .gmtime() => converts seconds since the Epoch. Returns a time tuple 
        # eg. (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        # strftime() => converts a time tuple to a string according the format provided
        print(f"Time taken: {time.strftime('%H:%M:%S', time.gmtime(difference))}")
        
        
        # if client is the one sending, then we need to wait for a response from server:
        if client_sending:
            wait_for_response(socket)
        
        
    # handle possible errors:
    except ConnectionResetError as CRE:
        if client_sending:
            print(f"The server requested exit. This could be because a file with the same filename already exists in the server or the server did not receive the filename correctly.")
        else:
            print("Client reset connection. This could be because a file with the same name was found in client folder.")
        
        # send ending byte: "|" indicating end of transmission:
        socket.send(END_TRANSMISSION.encode())
        # return false indicating error occurted to server/client so they can know and handle it accordingly:
        return False
        
        
    except FileNotFoundError as FNFE:
        print(f"The filename does not exist. Check that you spelled the name of the file correctly and try again.")

        # send ending byte: "|" indicating end of transmission:
        socket.send(END_TRANSMISSION.encode())
        # return false indicating error occurted:
        return False
        
        
    except MemoryError as ME:
        print(f"Program ran out of memory. Make sure that the filename of the file is not too long. If you keep getting this error, check that you have enough ram available to run this code in your computer.")

        # send ending byte: "|" indicating end of transmission:
        socket.send(END_TRANSMISSION.encode())
        # return false indicating error occurted:
        return False
        
        
    except Exception as e:
        print(f"An unexpected error occurred.. ")
        print(e)
        
        # send end transmission message indicating to stop:
        socket.send(END_TRANSMISSION.encode())

        # return false indicating error occurted:
        return False
    
    
    # if all were fine, return true indicating success:
    else:
        return True
    
    
#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_file(socket, FILENAME=""):
    """Receive a file over the socket provided.
    If server is receiving: firstly, receive the filename then make the file and write data to it.
    If client is receiving: make the file then wait for data coming from server and write it to file.

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.
        FILENAME (str, optional): The filename to be sent over the socket. If server is the one receiving, leave it as default value.. Defaults to "".

    Raises:
        ValueError: If server could not find the filaname from the data streams client sends, a ValueError will raise.
        FileExistsError: If server or client are receiving a file with the same filename of another file in their folder, a FileExistsError will raise.

    Returns:
        boolean: True indicates success and False indicates a problem.
    """
    
    # get current time. This is just to calculate how long the code will take to execute:
    start_time = time.time()
    
    END_FILENAME, END_TRANSMISSION = "|", "|" # indicates end of transmission:

    try:
        
        # if FILENAME is not specified, that mean the server is receiving and client is sending
        # in this case, client will send the filename just before file data so we will capture it by recv_filename():
        if FILENAME == "":
            # this var is just to be used later to call wait_for_response() to get a response from server or not:
            client_recv = False
            # capture filename and any extra data that was send with the data stream
            FILENAME, data = recv_filename(socket, END_FILENAME)
            
            # recv_filename will return (0,0) if any error happened or it could not get a proper filename with an extension at the end of it:
            if FILENAME == 0 and data == 0:
                raise ValueError


        # elif FILENAME is specified, that means the server is sending and client is receiving
        # so we need to send the filename to the server now:
        else:
            # this var is just to be used later to call wait_for_response() to get a response from server or not:
            client_recv = True
            
            # "|" indicates end of filename:
            to_send = FILENAME + "|"
            socket.send(to_send.encode())
            
            # this to be used later to just start a while loop:
            data = bytearray(1)
            
            
        # ----------------- at this stage, we have got a FILENAME and data -------------------------
        
        
        # check if filename exists by getting the filenames in the current directory
        filenames = get_filenames()
        if FILENAME in filenames:
            raise FileExistsError
        
        # open file in write binary mode
        # if filename does not exist, create the file:
        with open(FILENAME, 'wb') as f:
            
            # if we have captured extra data that was sent with the filename, we will write it now before receiving the rest of the data:
            if data != bytearray(1):
                f.write(data)
                # flush the file now so we can write more data to it later in the while loop:
                f.flush()
                

            # we will only break if we have got the "|" at the end of the data
            # the while loop will always start as data will always be either bytearray(1) OR actual data:
            while len(data) > 0:
                # max of 4096 bytes is used for compability with different OS:
                data = socket.recv(4096)
                
                # if data ends with "|", write the data to the file without the last byte:
                if (data.endswith(END_TRANSMISSION.encode())):
                    f.write(data[:-1])
                    break
                
                else:
                    f.write(data)
                    # flush the file now so we can write to it again in the next iteration:
                    f.flush()
                    
        
        # print time taken to excute to receive the file:
        finish_time = time.time()
        difference = finish_time-start_time
        # print the time taken to execute the function in a nicely formatted way:
        # .gmtime() => converts seconds since the Epoch. Returns a time tuple 
        # eg. (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
        # strftime() => converts a time tuple to a string according the format provided
        print(f"Time taken: {time.strftime('%H:%M:%S', time.gmtime(difference))}")
        
        
        # if the client is the one receiving, that means the server will send a response reporting on its status:
        if client_recv:
            wait_for_response(socket)
            
            
    # handle exceptions:
    except FileExistsError as FEE:
        report = "A file with the same name already exists."
        print(report)
        return False
    
    except ValueError as VE:
        print("Server could not differentiate the filename in the data sent by client.")
        return False
        
    except Exception as e:
        print(f"An unexpected error occurred.. ")
        print(e)
        # return false indicating error occurred:
        return False
    
    
    # if all were fine, return true indicating success:
    else:
        return True
    
    
#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def send_listing(socket):
    """Sends a listing to client of all the files in current server's directory. Filenames will be seperated by "|"

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.

    Returns:
        boolean: True indicates success and False indicates a problem.
    """
    
    try:
        # get_filenames returns a list of all the files in the current directory:
        filenames = get_filenames()
        print(f"Filenames found: {filenames}")
        
        # filter out the irrelevant content from the list (eg. folder names)
        # send each filename seperately (by "|" after each filename):
        for filename in filenames:
            # sendall() is used just in case the filename is too long:
            socket.sendall(filename.encode())
            socket.send(b'|')
        
                
    # handle errors:
    except (ConnectionAbortedError, ConnectionResetError) as CE:
        print("Client requested exit before sending all the data.")
        # return false indicating error occurred:
        return False
    
    except OSError as OSE:
        print("The socket has closed unexpectedly.")
        # return false indicating error occurred:
        return False
        
    except Exception as e:
        print(f"An unexpected error occurred..")
        print(e)
        # return false indicating error occurred:
        return False
    
    # if all were fine, return true indicating success:
    else:
        return True


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_listing(socket):
    """Receives a listing of all the files in the server's directory. Filenames will be seperated by "|"

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.

    Returns:
        boolean: True indicates success and False indicates a problem.
    """
    
    try:
        # this var to be used to start the while loop:
        data = bytearray(1)
        
        # print a starter message:
        print(f"Files available: ")

        # recv will give us b'' when sending is finished and that has len = 0
        # so when we get this, we will stop receiving more data:
        while len(data) > 0:
            # max of 4096 bytes is used for compability with different OS:
            data = socket.recv(4096)
            # split the data by a seperator "|":
            files = data.split(b'|')
            
            # if data is not empty (empty indicating end of transmission):
            if data != b'':
                for file in files:
                    # only print if filename is not empty (usually the last element in the list will be empty because of .split()):
                    if file != b'':
                        print(file.decode())
            
            # if we reached end of transmission:
            elif data == b'':
                return True
    
    
    except (ConnectionAbortedError, ConnectionResetError) as CE:
        print("Server requested exit before sending all the data.")
        # return false indicating error occurred:
        return False
    
    except OSError as OSE:
        print("The socket has closed unexpectedly.")
        # return false indicating error occurred:
        return False
    
    except Exception as e:
        print(f"An unexpected error occurred..")
        print(e)
        # return false indicating error occurred:
        return False


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_filename(socket, END_FILENAME):
    """Receives the filename from the first data streams to be read/wrote by another functions.

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.
        END_FILENAME (str): The byte that will be used to indicate the end of the filename sent.

    Returns:
        tuple: Containing (filename, data) where the filename is the filaname received with its extension and data is any extra data that was received just after the filename. Extra data needs to be returned to it can be written to the file by another function.
    """
       
    # encode it so we can use it in the while loop to check data:
    END_FILENAME = END_FILENAME.encode()

    # max of 4096 bytes is used for compability with different OS:
    recv_rate = 4096

    # this to be used to just start a while loop:
    data = bytearray(1)
    while len(data) > 0:
        
        data = socket.recv(recv_rate)
        
        # set filename as a copy of data:
        FILENAME = data[:]
        
        # if filename is short, END_FILENAME will be present in the same data stream:
        if END_FILENAME in data:
            
            # strip out everything after END_FILENAME from FILENAME:
            end_index = FILENAME.index(END_FILENAME)
            FILENAME = FILENAME[:end_index]
            
            # strip out the FILENAME and END_FILENAME from data so we can return it to be written to the file:
            # eg. if data = "helloworld.txt|12345", it will return "12345"
            # if data = "helloworld.txt|", it will return ""
            end_index = data.index(END_FILENAME) + len(END_FILENAME)
            data = data[end_index:]
            
            # stop receiving data:
            break
        
            
        # if filename is too long
        elif (END_FILENAME.encode() not in data):
            
            # loop until END_FILENAME is received:
            while END_FILENAME.encode() not in data:
                data = socket.recv(recv_rate)
                FILENAME += data
            
                # strip out everything after END_FILENAME from FILENAME:
            end_index = FILENAME.index(END_FILENAME)
            FILENAME = FILENAME[:end_index]
            
            # strip out the FILENAME and END_FILENAME from data so we can return it to be written to the file:
            # eg. if data = "helloworld.txt|12345", it will return "12345"
            # if data = "helloworld.txt|", it will return ""
            start_index = data.index(END_FILENAME) + len(END_FILENAME)
            data = data[start_index:]
            
            # stop receiving data:
            break
            
            
        # if nothing is left after END_FILENAME, set data to bytearray(1) so we return data with len > 0 (this to be used in recv_file() or send_file()):
    if data == b'':
        print("data is empty")
        data = bytearray(1)

    # check that we have actually got a filename with an extension:
    FILENAME = FILENAME.decode()
    name, extension = os.path.splitext(FILENAME)
    
    # check that the extension of the file is not empty (means there is no extession received) and extenssion is not only a dot (means either full extenssion is not received OR no file type is received; such as .txt/.png)
    # then return the filename and any extra data now:
    if extension != "" and extension != ".":
        print(f"returning filename and data: {FILENAME} - {data}")
        return (FILENAME, data)
    
    # if above conditions apply, return (0,0) indicating error:
    else:
        print("returning 0,0")
        return (0,0)


#* ------------------------------------------------------------------------------------------------------------------------------------------------------

def get_filenames():
    """Gets a list of all the filenames in the current directory. Gets only the name of the files, not the folders.

    Returns:
        list: Containing all the filenames found in the directory.
    """
    
    # os.getcwd() => is our current directory
    # join() => joins the paths with the filename and returns an absolute path for each file to be used in isfile()
    # isfile() => takes an absolute path and return True/False if this path is a regural file or not
    # listdir() => returns a list of all the contents in this directory
    # eg. ['.vscode', 'common_functions.py', 'server-img-2.jpg', 'server-img.png', 'server-text-file.txt', 'server.py', '__pycache__']
    filenames = [file for file in listdir(os.getcwd()) if isfile(join(os.getcwd(), file))]
    return filenames


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def wait_for_response(socket):
    """Waits for a final response from the server to report on its status.

    Args:
        socket (Socket): Client predefined socket to be used for communication between server and client.
    """
    
    print(f"Waiting for a response from server..")
    # the server will not send a response bigger than 4096 bytes so no while loop is needed:
    data = socket.recv(4096)    
    print(data.decode())


#* ------------------------------------------------------------------------------------------------------------------------------------------------------
