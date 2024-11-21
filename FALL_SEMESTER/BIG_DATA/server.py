import socket
import sys
import kvServerlib as server
import Codes

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.socket.settimeout(0.5)
        self.socket.bind((self.host, self.port)) 
        self.trie_dict = None

    def check_query_type(self, packet_row_str, initial_trie_dict):
        query_comm = packet_row_str[0].strip()
        query_res = " "
        if query_comm == "PUT":
             server.PUT(packet_row_str[1], initial_trie_dict)
        elif query_comm == Codes.REQUESTS_LI[0]:
             query_res = server.GET(packet_row_str[1], initial_trie_dict)
        elif query_comm == Codes.REQUESTS_LI[2]:
             query_res = server.DELETE(packet_row_str[1], initial_trie_dict)
        elif query_comm == Codes.REQUESTS_LI[1]:
             query_res = server.QUERY(packet_row_str[1], initial_trie_dict)
        elif query_comm == Codes.REQUESTS_LI[3]:
             query_res = server.COMPUTE(packet_row_str[1], initial_trie_dict)
        else:
             print("Wrong query format")
        return query_res

    def initialize_server(self, initial_trie_dict):
        while True:
            self.socket.listen()
            #self.socket.settimeout(0.5)
            conn, _ = self.socket.accept()

            while conn:
                print(f"Host {self.host} connected\n")
                buffer_max_size = 4096000
                packet = conn.recv(buffer_max_size)
                packet_decoded = packet.decode()
                packet_decoded += conn.recv(buffer_max_size).decode()
                packet_decoded = packet_decoded[:-8]
                buffer_max_size = int(packet_decoded)
                conn.sendall(Codes.SUCCESS.encode("utf-8"))
                conn.sendall(b"finished")

                while True:
                    packet = conn.recv(buffer_max_size)
                    packet_decoded = packet.decode()
                    packet_decoded += conn.recv(buffer_max_size).decode() # empty buffer
                    packet_decoded = packet_decoded[:-8]
                    if not packet:
                        break
                    if ("exit" in packet_decoded) or ("EXIT" in packet_decoded):
                        # self.socket.settimeout(0.5) doesn't work on exit
                        print("The application will now exit")
                        sys.exit()
                    try:
                        packet_row_str = packet_decoded.split(" ", 1)
                        if len(packet_row_str) < 2:
                           print("Wrong query format")
                        query_res = Server.check_query_type(self, packet_row_str, initial_trie_dict)
                        send_packet_to_client = query_res.encode() # encode query result
                        conn.sendall(send_packet_to_client)
                        conn.sendall(b"finished")
                    except:
                        conn.sendall(Codes.NOT_FOUND.encode("utf-8"))
                        conn.sendall(b"finished")
