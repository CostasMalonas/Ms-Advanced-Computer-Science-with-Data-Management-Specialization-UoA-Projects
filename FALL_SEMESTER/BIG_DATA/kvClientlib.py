import subprocess
import Codes
import os
import sys
import socket
import time
import threading
from tqdm import tqdm
import random

def check_input_data(argument_list):
    if argument_list[1] != '-s':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif not os.path.exists(argument_list[2]):
        print('SERVER FILE NOT EXIST')
        sys.exit()
    elif argument_list[3] != '-i':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif not os.path.exists(argument_list[4]):
        print('DATA FILE NOT EXIST')
        sys.exit()
    elif argument_list[5] != '-k':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif not argument_list[6].isnumeric():
        print('WRONG INPUT EXPECTED NUMBER')
        sys.exit()
    else:
        return argument_list[2], argument_list[4], int(argument_list[6])


def get_data_file_lines(datafile):
    with open(datafile, 'r') as f:
        lines = [line.strip() for line in f]
    return lines


def thread_fun(host, port):
    """
    Call the kvServer.py file and initialize server objects
    """
    args = []
    args.append(Codes.python)
    args.append(Codes.server_script)
    args.append(Codes.flags[0])
    args.append(host)
    args.append(Codes.flags[1])
    args.append(port)
    subprocess.run(args, capture_output=False)

def connect_to_servers(serverFile_path):
    """
    Function that create the threads and returns the list with the threads created.
    Each thread calls the thread_fun function wich executes the kvServer.py file
    and creates Server objects
    """
    # create a list with tuples in the format (host, port)
    host_ports_ls = [(line.strip().split()) for line in get_data_file_lines(serverFile_path)] 
    # print('host_port: ', host_ports_ls, '\n')
    # host_ports_dict = {} # dictionary with hosts as keys and ports as values
    # for host_port in host_ports_ls:
    #     host_ports_dict[host_port[0]] = host_port[1]
    # print('host_ports_dict: ', host_ports_dict, '\n')
    thread_ls = []
    # create a thread, call the thread_fun function and 
    # create a server object
    for tup in host_ports_ls:
        thread_ls.append(threading.Thread(target=thread_fun,args=(tup[0], tup[1])))
    return thread_ls

def get_host_ports_list(serverFile):
    """
    A function that returns a list where each value is a tuple
    in the format (host port)
    """
    with open(serverFile) as f:
        lines = [(line.strip().split()) for line in f]
    return lines

def is_thread_alive(thread_ls):
    """
    Function that returns the number of dead threads
    """
    dead_th = 0
    for th in thread_ls:
        if not th.is_alive():
            dead_th += 1
    return dead_th

def initialize_socket_threads(thread_ls, host_port_ls):
    """
    Function that takes as input parameters the list with 
    the thread objects created and the list with the (host, port) tuples,
    creates a list with socket objects and connect to each host from the host_port_ls
    """
    socket_ls = [socket.socket() for th in thread_ls]
    for i in range(len(socket_ls)):
        try:
            socket_ls[i].connect(( host_port_ls[i][0], int(host_port_ls[i][1])))
            #socket_ls[i].settimeout(0.5)
        except:
            sys.exit()
    return socket_ls


def inspect_query(query_str, thread_ls):
    """
    Function that takes as parameters the query string and the list with the threads,
    checks if the string is in the right format and if we have enough servers running
    and returns the command and the query list that has as first value the command string
    and as second value the data query
    """
    query_ls = query_str.strip().split(" ", 1)
    query_comm = query_ls[0]
    dead_thread = is_thread_alive(thread_ls)
    if (len(query_ls) < 2 and (query_comm in Codes.REQUESTS_LI)):
        print(f"{query_ls[0]} query is missing values")
    elif (len(query_ls) < 2 and (any(query == query_comm for query in Codes.REQUESTS_LI)==False)) or (len(query_ls[1].split(" ")) > 1 and query_comm != 'COMPUTE'):
        print(f"{query_ls[0]} query command doesn't exist")
    # elif query_comm in [Codes.REQUESTS_LI[0], Codes.REQUESTS_LI[1], Codes.REQUESTS_LI[2]] and dead_thread != 0:
    #     print(f"CAUTION { dead_thread } servers are down")
    elif dead_thread == len(thread_ls):
        print('No servers alive')
        sys.exit()
    elif query_comm == Codes.REQUESTS_LI[2] and dead_thread:
        print("No servers alive")
        sys.exit()
    return query_comm, query_ls

def check_delete_query(server_answers_ls, query_ls):
    """
    Function that checks if the deletion of a key was succesful or not.
    It checks the answer of the server and shows the according message.
    """
    if Codes.SUCCESS in server_answers_ls:
        print(f"{query_ls[1]} deleted")
    elif Codes.SUCCESS not in server_answers_ls and len(query_ls) >= 2:
        print(f"{query_ls[1]} not found ")
    else:
        print("Please type a key for deletion")

def send_query_to_server(socket_ls, query_str, thread_ls, buffer_max_size, k):
    """
    Function that first encodes the query string, sends it over the sockets to each server
    (if the thread is alive) and at the end send a message that it finished sending.
    Then receives the answer from the server, decodes it and appends it in server_answers_ls list.
    If the query command was DELETE it checks if the deletion was succesful or not. If it was another
    query command it checks if the server list contains the answer to the query, if not it shows the 
    according message. If both of the above cases are not true it filters out the server answers
    and return the string with the answer.
    """
    query_comm, query_ls = inspect_query(query_str, thread_ls)
    query_command_str = " ".join(query_ls).encode() # string query command to send 
    server_answers_ls = [] # answers of server, 404 etc
    for sock, thread in zip(socket_ls, thread_ls): # check if thread alive if yes send
        if thread.is_alive():
            sock.sendall(query_command_str)
            sock.sendall(b"finished")
            received_packet = sock.recv(buffer_max_size) # received packet from server to be decoded
            received_packet_decoded = received_packet.decode()
            received_packet_decoded += sock.recv(buffer_max_size).decode()
            received_packet_decoded = received_packet_decoded[:-8]
            server_answers_ls.append(received_packet_decoded)
    if query_comm == Codes.REQUESTS_LI[2]:
        check_delete_query(server_answers_ls, query_ls)
    elif server_answers_ls.count(" ") == len(server_answers_ls):
        print(f"{query_ls[1]} doesn't exist or the query didn't execute correctly")
    else:
        server_answer = []
        for ans in server_answers_ls:
            if ans not in [" ", Codes.SUCCESS, Codes.NOT_FOUND]:
                server_answer.append(ans)
        answer = ''.join(server_answer)
        answer_len = len(answer)/k
        #print(type(answer_len))
        #print(answer_len)
        print(answer[:int(answer_len)])


def execute_query_commands(socket_ls, thread_ls, buffer_max_size, k):
    """
    Function that awaits for a user input (query) and calls the send_query_to_server function
    to execute the query and get the answer.
    """
    while True:
        if is_thread_alive(thread_ls) == 0:
            user_input = input("\n\nType one of "+str(Codes.REQUESTS_LI) + ": ")
            if "exit" in user_input.lower():
                print('The application will now exit')
                sys.exit()
            send_query_to_server(socket_ls, user_input, thread_ls, buffer_max_size, k)
        else:
            print(f"{is_thread_alive(thread_ls)} servers are down. Correct results not quaranteed\n")
            user_input = input("\n\nType one of "+str(Codes.REQUESTS_LI) + ": ")
            if "exit" in user_input.lower():
                print('The application will now exit')
                sys.exit()
            send_query_to_server(socket_ls, user_input, thread_ls, buffer_max_size, k)


def find_buffer_maximum_size(datafilepath):
    """
    A function that returns the buffers maximum size
    that is calculated from the size of the data file
    """
    return os.stat(datafilepath).st_size

def send_buffer_maximum_size(socket_ls, thread_ls, buffer_max_size):
    if is_thread_alive(thread_ls) == len(thread_ls):
        print("The application will now exit. Servers are down")
        sys.exit()
    for sock in socket_ls:
        #sock.settimeout(0.5)
        sock.sendall(str(buffer_max_size).encode())
        sock.sendall(b"finished")
        #empty buffer
        received_packet_decoded = sock.recv(buffer_max_size).decode()
        received_packet_decoded+= sock.recv(buffer_max_size).decode()


def send_packet_to_server(thread_ls, packet, k, socket_ls, buffer_max_size):
    """
    Function that checks if any threads alive,
    sends the maximum buffer size over the socket and
    calls the prepare_packet_to_send function that sends the
    data packets (PUT) at the random servers
    """
    if is_thread_alive(thread_ls) == len(thread_ls):
        print("No servers avaible. The program will now exit")
        sys.exit()
    time.sleep(0.1) 
    send_buffer_maximum_size(socket_ls, thread_ls, buffer_max_size)
    print("Send packet to server")
    prepare_packet_to_send(packet, socket_ls, k, buffer_max_size)
    

def prepare_packet_to_send(packet, socket_ls, k, buffer_max_size):
    """
    Form the PUT queries, choose a random socket and call the
    send encoded packet function to send the data packet
    """
    #print(len(socket_ls))
    for row in tqdm(packet):
        packet_str = "PUT" + " " + row
        packet_str_encoded = packet_str.encode()
        random_sockets = random.sample(socket_ls, k)
        send_encoded_packet(random_sockets, packet_str_encoded, buffer_max_size)

def send_encoded_packet(random_sockets, packet_str_encoded, buffer_max_size):
    for socket in random_sockets:
        socket.sendall(packet_str_encoded)
        socket.sendall(b"finished")
        socket.recv(buffer_max_size)
        socket.recv(buffer_max_size).decode()





           