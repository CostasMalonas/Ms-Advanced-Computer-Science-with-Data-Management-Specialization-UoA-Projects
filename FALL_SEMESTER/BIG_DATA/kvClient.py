import kvClientlib as client 
import sys



argument_list = sys.argv
serverFile_path, dataToIndex_path, k = client.check_input_data(argument_list)

data_file_lines = client.get_data_file_lines(dataToIndex_path)
# create server object for each thread
thread_ls = client.connect_to_servers(serverFile_path)


# Take each thread from the thread list and initiate it
for thread in thread_ls:
    thread.start()
    thread.join(0.1) # If I leave join empty client doesn't execute

# get host ports list 
host_port_ls = client.get_host_ports_list(serverFile_path) 
buffer_max_size = client.find_buffer_maximum_size(dataToIndex_path) # calclate the maximum buffer size    
socket_ls = client.initialize_socket_threads(thread_ls, host_port_ls) # initialize connections
#print('LEN: ',len(socket_ls))
client.send_packet_to_server(thread_ls, data_file_lines, k, socket_ls, buffer_max_size) # send packets(data) to k rand servers
client.execute_query_commands(socket_ls, thread_ls, buffer_max_size, k)
