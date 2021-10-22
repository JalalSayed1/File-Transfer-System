import time
import os
from os import listdir
from os.path import isfile, join
import traceback

#! add description comment to all the functions

def send_file(socket, FILENAME=""): #! check that the filename exists and need to make send_file like recv_file, to get the filename from data stream
    try:
        # get current time. this is just for fun to calculate how long the code will take to execute:
        start_time = time.time()

        # if FILENAME is not specified, that mean the server will send the file and client will receive it
        # this means the client will be sending the FILENAME required before sending the data so we will capture it by recv_filename()
        if FILENAME == "":
            # recv_filename will return the filename and any extra data was received with the filename stream
            # we know that client will not send any data as client want to GET the file
            # so we will not use it and put it to a dummy var _
            FILENAME, _ = recv_filename(socket)
            
        # if FILENAME is specified, that means the server will receive the file and client will send that file
        # so we will send the "START_FILENAME" + FILENAME + "END_FILENAME" to the server now:
        else:
            print(f"filename was passed..")    
            m = "START_FILENAME" + FILENAME + "END_FILENAME"
            print(f"filename sent is: {m}", flush=True)
            socket.send(m.encode())
            
        # time.sleep(0.1)
        # socket.sendall("START_FILENAME".encode())
        # socket.sendall(filename.encode())
        # socket.sendall("END_FILENAME".encode())

        # open the required file in read binary mode:
        with open(FILENAME, 'rb') as f: #! check if file does not exist and error "MemoryError" for very big files and check if file exists so we do not write to it (maybe use list_items func bellow) and change the filename and check for FileExistsError error
            # send the file using the provided socket and return how many bytes has been sent:
            for data in f:
                # print(f"Sending a part of the file: {data.decode()}")
                socket.sendall(data)
        
        # send "END_TRANSMISSION" indicating that all data has been sent:
        socket.send(b'END_TRANSMISSION')
        
        
        finish_time = time.time()
        difference = finish_time - start_time
        print(flush=True) # just a blank line
        # print the time taken to execute the function in a nicely formatted way:
        # .gmtime() => converts seconds since the Epoch. Returns a time tuple
        # strftime() => converts a time tuple to a string according the format provided
        print(time.strftime('%H:%M:%S', time.gmtime(difference)), flush=True)
        
    # handle possible errors:
    except Exception as e: #! ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host AND check what are the possible errors
        print(e, flush=True)
        print(traceback.format_exc())
        # send end transmission message indicating to stop:
        socket.send(b'END_TRANSMISSION')
        # return false indicating error occurted:
        return False
    
    # if all were fine, return true indicating success:
    else:
        return True
    
    
#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_file(socket, FILENAME=""):

    # get current time. this is just for fun to calculate how long the code will take to execute:
    start_time = time.time()
    
    try:
        # # if filename is not passed (means action word is PUT and the server will receive a file), it means it will be passed with the data flow
        # # after this if statement, we will have the "FILENAME" and "data":
        # if FILENAME == "":
        #     print(f"Filename is left empty in recv_file()")
        #     # filename will be in between START_FILENAME and END_FILENAME (client must send it in this format):
        #     START_FILENAME, END_FILENAME = "START_FILENAME", "END_FILENAME"
        #     # got_filename to be used in the if statements to check if we received full filename or not yet
        #     got_filename = False

        #     data = bytearray(1)
        #     while len(data) > 0:
                
        #         # print(f"len of data is {len(data)} and data is: {data.decode()}")
                
        #         #! data might be splitted. eg. 4096 is just for START_FILENAME and another 4096 is just for FILENAME and so on
        #         data = socket.recv(4096)
                
        #         # print(f"just got some more data: {data.decode()}")
                
        #         # NB: max filename in windows is 255-260 characters, 255 characters in MacOS but 255 "bytes" in Linux.
        #         # store the filename which will be just after START_FILENAME:
        #         if START_FILENAME.encode() in data:#START_FILENAME.encode() in data / .decode()
        #             # print(f"starter for filename found in {data.decode()}")
        #             # data_decoded = data.decode()
        #             # get the index of the first charecter of the filename:
        #             start_index = data.index(START_FILENAME.encode()) + len(START_FILENAME.encode())
                    
        #             # filename is from start_index to the end of the data stream
        #             # we could have a short filename which will be sent in a single send() request or a long filename which will be sent via multiple send() requests
        #             # we will be checking on this very shortly
        #             FILENAME = data[start_index:]
                    
        #             # if filename is short, END_FILENAME will be present in the same data stream:
        #             if END_FILENAME.encode() in data: #END_FILENAME.encode() in data / .decode()
        #                 print(f"filename is short so recv_file() fount END_FILENAME in the same data stream")
        #                 # print(f"Current filename I have: {FILENAME}")
        #                 # strip it out from the FILENAME:
        #                 len_END_FILENAME = len(END_FILENAME)
                        
        #                 # this end_index is for the FILENAME to strip out everything after END_FILENAME words:
        #                 end_index = FILENAME.index(END_FILENAME.encode())
        #                 FILENAME = FILENAME[:end_index]
        #                 print(f"Stripped filename is: {FILENAME}")
                        
        #                 # strip out the FILENAME and END_FILENAME from data so we can use it later for writing the file:
        #                 end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
                        
        #                 # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345"
        #                 # if data = "helloworld.txtEND_FILENAME", it will return "" 
        #                 # if "" is returned, make data = bytearray(1) so it has a len > 0:
        #                 data = data[end_index:]
        #                 if data == b'': # data_decoded.endswith(END_FILENAME) # if nothing is after END_FILENAME
        #                     print(f"nothing is after END_FILENAME")
        #                     data = bytearray(1)
        #                     # print(f"data is now: {data}")
        #                 # else: # if we have some data after END_FILENAME
        #                 #     data = data[end_index:]
        #                 #     print(f"Found some data after END_FILENAME: {data}")
        #                     # if len(data) == 0:
        #                     #     data = bytearray(1)
                        
        #                 # decode the filename now because we got all of it:
        #                 FILENAME = FILENAME.decode()
        #                 print(f"final filename = {FILENAME}")
        #                 print(f"final data = {data}, len = {len(data)}")
                        
        #                 # break to start the file writing process:
        #                 break
                        
                    
        #             # if filename is too long
        #             # this block will run if END_FILENAME is not present in data and we have not got the full filename yet:
        #             elif (END_FILENAME not in data_decoded) and (not got_filename):
        #                 print(f"filename is not short enough to be sent in one data stream..")
        #                 # in case the filename is too long, it will be sent on multiple send requests so we need a while loop to store the filename after each recv call:
        #                 FILENAME += data_decoded
                        
        #                 print(f"looping to try get the full FILENAME now. Condition to start the while loop is {END_FILENAME.encode() not in data}.")
        #                 # loop until END_FILENAME is received:
        #                 while END_FILENAME.encode() not in data:
        #                     data = socket.recv(4096)
        #                     data_decoded = data.decode()
        #                     FILENAME += data_decoded
                            
        #                     # if END_FILENAME in data_decoded:
        #                     #     # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
        #                     #     FILENAME = FILENAME[:len(END_FILENAME)]
                        
        #                 # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
        #                 print(f"filename I have now is {FILENAME}")
        #                 FILENAME = FILENAME[:-12]#len(END_FILENAME)
        #                 print(f"filename after stripping is {FILENAME}")
        #                 # strip out the FILENAME + END_FILENAME from data so we can use it later for writing the file:
        #                 end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
        #                 # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345":
        #                 data = data[end_index:]
        #                 # break to start start the file writing process:
        #                 break
                    
        #         else:
        #             print(f"data we got: {data}")
        #             print(f"starter for filename not found in data.")

        # # if filename is passed, set data as a dummy non-zero byte to be used later to start a while loop:
        # else:
        #     print(f"filename was passed..")
        #     data = bytearray(1)
        
        
        
        #  if FILENAME is not specified, that mean the server will receive the file and client will send it
        # this means the client will be sending the FILENAME required before sending the data so we will capture it by recv_filename()
        if FILENAME == "":
            FILENAME, data = recv_filename(socket)

        # if FILENAME is specified, that means the server will send the file and client will receive that file
        # so we will send the "START_FILENAME" + FILENAME + "END_FILENAME" to the server now:
        else:
            print(f"filename was passed..")
            m = "START_FILENAME" + FILENAME + "END_FILENAME"
            print(f"filename sent is: {m}", flush=True)
            socket.send(m.encode())
            data = bytearray(1)
            
            
        # ----------------- at this stage, we must have the values for FILENAME and data -------------------------
        
        
        
        # check if filename exists or not:
        # get the filenames in the current directory
        # could have used os.path.exists(path) but wanted to reuse my existed code
        filenames = get_filenames() #! check for PUT request that this is working
        if FILENAME in filenames:
            print(f"filename exists.")
            raise FileExistsError
        
        # create a new file only if the file does not exist. If file exists, it would have return an FileExistsError from above code
        with open(FILENAME, 'ab') as f: #! check if file does not exist and error "MemoryError" for very big files and check if file exists so we do not write to it (use os.path.exists(path)) and change the filename and check for FileExistsError error
            print(f"Writing to the file..")
            # print(f"data we are starting with is: {data} len = {len(data)}")
            # a new non-zero variable (string of bytes) to use it in the while loop:
            # data = bytearray(1)
            
            # write the data we have got from above code if filename was capture via the data flow:
            # this ensures we do not write the byte b'1' from data = bytearray(1) to the file:
            if data != bytearray(1):
                print(f"we have some data from before so we will write it to the file now..")
                f.write(data)
                # flush the file now so we can write more data to it later in the while loop:
                f.flush()
                
            # a variable indicates end of transmission:
            END_TRANSMISSION = "END_TRANSMISSION"

            # recv will give us b'' when transmission is finished and that has len = 0
            # so when we get this, we will stop receiving data:
            print(f"starting a while loop to receive the rest of the data..")
            
            while not data.endswith(END_TRANSMISSION.encode()): #!len(data) > 0:
                data = socket.recv(4096)
                data_list = data.split(b"\n")
                # print(f"Just received some data: {data}, type = {type(data)}")
                # print(f"data list is: {data_list}")
                
                # check if data ends with END_TRANSMISSION, write it to the file but without the ending ("END_TRANSMISSION")
                if data.endswith(END_TRANSMISSION.encode()):
                    # write what we just received to file:
                    len_END_TRANSMISSION = len(END_TRANSMISSION)
                    f.write(data[:-len_END_TRANSMISSION])
                
                # if data does not end with "END_TRANSMISSION", simply just write data to file:
                else:
                    f.write(data)
                    
                # flush the file everytime new data is written to it:
                # print(f"trying to flush the file..")
                f.flush()
                

            print(f"while loop is finished")
        # print time taken to excute this function:
        finish_time = time.time()
        difference = finish_time-start_time
        # check if the difference were 0, that means this function has run only for a final check
        # the function runs after receiving all the data for a final time
        # only if difference != 0, print the time:
        if difference != 0:
            print(flush=True) # just a blank line
            # print the time taken to execute the function in a nicely formatted way:
            # .gmtime() => converts seconds since the Epoch. Returns a time tuple
            # strftime() => converts a time tuple to a string according the format provided
            print(time.strftime('%H:%M:%S', time.gmtime(difference)), flush=True)
             
    # handle exceptions:
    except FileExistsError as FEE:
        message = f"A file with the same name already exists."
        # print message to server's screen:
        print(message, FEE, flush=True)
        #! would be nice if I can send this message to the client
        return False
        
    except Exception as e: #! check what are the possible errors
        print(e, flush=True)
        print(traceback.format_exc())
        # return false indicating error occurred:
        return False
    
    # if all were fine, return true indicating success:
    else:
        return True
    
    
#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def send_listing(socket):
    
    try:
        # get_filenames returns a list of all the files in the current directory:
        filenames = get_filenames()
        print(f"filenames found: {filenames}")
        # print report header message:
        print(f"These file names have been found and sent:", end=" ", flush=True)
        
        # filter out the irrelevant content from the list and return send each file name seperately:
        # eg. returns: ['common_functions.py', 'server-img.png', 'server-text-file.txt', 'server.py']
        for filename in filenames:
            # complete report message by print this filename:
            print(f"{filename}", end=", ", flush=True)
            # sendall() is used just in case the filename is too long:
            socket.sendall(filename.encode())
        
                
    # handle errors:
    except Exception as e: #! check what are the possible errors
        print(e, flush=True)
        print(traceback.format_exc())
        # return false indicating error occurred:
        return False
    
    # if all were fine, return true indicating success:
    else:
        return True


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_listing(socket):
    try:
        # "data" to be used in the while loop, we need a non 0 byte to start with:
        file = bytearray(1)
        
        # print a starter message:
        print(f"Files available: ", flush=True)

        # recv will give us b'' when sending is finished and that has len = 0
        # so when we get this, we will stop receiving data:
        while len(file) > 0:
            # 4096 bytes is used for compability with different OS
            file = socket.recv(4096)
            # b'' indicates end of transmission:
            if file != b'':
                # print each file in a separate line
                print(f"{file.decode()}", flush=True)
            
            # if we reached end of transmission, return true:
            elif file == b'':
                return True
            
            # if an error happend:
            else:
                raise Exception
            
    except Exception as e: #! check what are the possible errors
        print(e, flush=True)
        print(traceback.format_exc())
        return False


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


def recv_filename(socket):
    try:
        print(f"Filename is left empty in recv_file()")
        # filename will be in between START_FILENAME and END_FILENAME (client must send it in this format):
        START_FILENAME, END_FILENAME = "START_FILENAME", "END_FILENAME"
        # got_filename to be used in the if statements to check if we received full filename or not yet
        got_filename = False

        data = bytearray(1)
        while len(data) > 0:
        
            # print(f"len of data is {len(data)} and data is: {data.decode()}")
            
            #! data might be splitted. eg. 4096 is just for START_FILENAME and another 4096 is just for FILENAME and so on
            data = socket.recv(4096)
            
            # print(f"just got some more data: {data.decode()}")
            
            # NB: max filename in windows is 255-260 characters, 255 characters in MacOS but 255 "bytes" in Linux.
            # store the filename which will be just after START_FILENAME:
            if START_FILENAME.encode() in data:#START_FILENAME.encode() in data / .decode()
                # print(f"starter for filename found in {data.decode()}")
                # data_decoded = data.decode()
                # get the index of the first charecter of the filename:
                start_index = data.index(START_FILENAME.encode()) + len(START_FILENAME.encode())
                
                # filename is from start_index to the end of the data stream
                # we could have a short filename which will be sent in a single send() request or a long filename which will be sent via multiple send() requests
                # we will be checking on this very shortly
                FILENAME = data[start_index:]
                
                # if filename is short, END_FILENAME will be present in the same data stream:
                if END_FILENAME.encode() in data: #END_FILENAME.encode() in data / .decode()
                    print(f"filename is short so recv_file() fount END_FILENAME in the same data stream")
                    # print(f"Current filename I have: {FILENAME}")
                    # strip it out from the FILENAME:
                    len_END_FILENAME = len(END_FILENAME)
                    
                    # this end_index is for the FILENAME to strip out everything after END_FILENAME words:
                    end_index = FILENAME.index(END_FILENAME.encode())
                    FILENAME = FILENAME[:end_index]
                    print(f"Stripped filename is: {FILENAME}")
                    
                    # strip out the FILENAME and END_FILENAME from data so we can use it later for writing the file:
                    end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
                    
                    # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345"
                    # if data = "helloworld.txtEND_FILENAME", it will return "" 
                    # if "" is returned, make data = bytearray(1) so it has a len > 0:
                    data = data[end_index:]
                    if data == b'': # data_decoded.endswith(END_FILENAME) # if nothing is after END_FILENAME
                        print(f"nothing is after END_FILENAME")
                        data = bytearray(1)
                        # print(f"data is now: {data}")
                    # else: # if we have some data after END_FILENAME
                    #     data = data[end_index:]
                    #     print(f"Found some data after END_FILENAME: {data}")
                        # if len(data) == 0:
                        #     data = bytearray(1)
                    
                    # decode the filename now because we got all of it:
                    FILENAME = FILENAME.decode()
                    print(f"final filename = {FILENAME}")
                    print(f"final data = {data}, len = {len(data)}")
                    
                    # break to start the file writing process:
                    break
                
            
                # if filename is too long
                # this block will run if END_FILENAME is not present in data and we have not got the full filename yet
                # The following code could not be tested as the max filename length in our normal operating systems are:
                # in windows is 255-260 characters, 255 characters in MacOS and 255 "bytes" in Linux
                # in windows: it is possible to enable long file name support which makes us able to have filenames up to 32,767 characters but that is not what most people do
                elif (END_FILENAME.encode() not in data) and (not got_filename):
                    print(f"filename is not short enough to be sent in one data stream..")
                    # in case the filename is too long, it will be sent on multiple send requests so we need a while loop to store the filename after each recv call:
                    FILENAME += data
                    
                    print(f"looping to try get the full FILENAME now. Condition to start the while loop is {END_FILENAME.encode() not in data}.")
                    # loop until END_FILENAME is received:
                    while END_FILENAME.encode() not in data:
                        data = socket.recv(4096)
                        # data_decoded = data.decode()
                        FILENAME += data
                        
                        # if END_FILENAME in data_decoded:
                        #     # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
                        #     FILENAME = FILENAME[:len(END_FILENAME)]
                    
                    # FILENAME will always end with the END_FILENAME word (regardless the filename was long or short), so strip it out:
                    print(f"filename I have now is {FILENAME}")
                    FILENAME = FILENAME[:-12]#len(END_FILENAME)
                    print(f"filename after stripping is {FILENAME}")
                    # strip out the FILENAME + END_FILENAME from data so we can use it later for writing the file:
                    end_index = data.index(END_FILENAME.encode()) + len(END_FILENAME.encode())
                    # eg. if data = "helloworld.txtEND_FILENAME12345", it will return "12345":
                    data = data[end_index:]
                    # break to start start the file writing process:
                    break
                    
            else:
                print(f"data we got: {data}")
                print(f"starter for filename not found in data.")
            
    except Exception as e:
        print(e, flush=True)
        print(traceback.format_exc())
        return

    else:
        return (FILENAME, data)
    
            

#* ------------------------------------------------------------------------------------------------------------------------------------------------------

def get_filenames():
    """get a list of only the filenames in our current directory

    Returns:
        list: list contains the file names only, not folders
    """
    # os.getcwd() => is our current directory
    # listdir(os.getcwd()) => returns a list of all the contents in this directory
    # eg. ['.vscode', 'common_functions.py', 'server-img-2.jpg', 'server-img.png', 'server-text-file.txt', 'server.py', '__pycache__']
    # join(os.getcwd(), file) => joins the paths with the filename to return an absolute path for each file to be used in isfile()
    # isfile() => takes an absolute path and return True/False if this path is a regural file or not
    filenames = [file for file in listdir(os.getcwd()) if isfile(join(os.getcwd(), file))]
    return filenames


#* ------------------------------------------------------------------------------------------------------------------------------------------------------


#* EXTRA (for fun) function:
def calculate_bytes(num_of_bytes, suffix="B"):
    """a function just to calculate how many KB/MB/GB or TB of data we sent using number of bytes we provide it with

    Args:
        num_of_bytes (int): number of bytes
        suffix (str, optional): the suffix of the unit (eg. MB). Defaults to "B".

    Returns:
        [str]: the result from the calculations
    """
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num_of_bytes) < 1024.0:
            return f"{num_of_bytes:3.1f} {unit}{suffix}"
        num_of_bytes /= 1024.0
    return f"{num_of_bytes:.1f}Yi{suffix}"


#* ------------------------------------------------------------------------------------------------------------------------------------------------------






#* for testing:
# for send file:
# send_file(soc,  "server-text-file.txt")
# send_file(soc,  "server-img.png")
# for recv file:
# recv_file(soc, "img-copy.png")
# recv_file(soc, "windows11.iso")
# recv_file(srv_sock, "server-img.png")

# print((b'\x01\x02\x03') == (b'\x01\x02\x03').zfill(10))
# with open("server-img-2.jpg", 'rb') as f:
#     print(f.read()[-100:])
# with open("server-img.png", 'rb') as f:
#     print(f.read()[-100:])
# with open("server-text-file.txt", 'rb') as f:
#     print(f.read()[-100:])
# with open("server-img.png", 'rb') as f:
    # print(f.read()[-100:])
    # data = f.read()
    # print(type(data[-100:]))
    # for elt1 in data:
    #     for i, elt2 in enumerate (elt1):
    #         print(elt2)
    #         if elt1[i]+elt1[i+1]+elt1[i+2] == b"END":
    #             print("yes found it.. #######################")

# send_listing("")
# files = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
# print(files)
# print(os.getcwd())
# print(os.path.abspath(os.getcwd()))
# print(listdir(os.getcwd()))
# print()
# print()
# s="123helloworld456"
# start = "h"
# end = "4"
# i1 = s.index(start) + len(start)
# i2 = s.index(end)
# print(s[i1:i2])
# i = len("hello")
# out = s[i:]
# print(out)
# i = s.index(out) + len(out)
# print(i)

# print(len(("START_FILENAME" + "client-text-file.txt" + "END_FILENAME").encode()))
# print(len(b"17"))
# print(b'123' + b'45')
# s = "client-text.txtEND_FILENAME"
# print(len("END_FILENAME"))
# print(s[:-12])

# s = b"starting a\n while loop"
# print(s.split(b"\n"))

# print(b'1'*4096)
# print(len("client-img-1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"))