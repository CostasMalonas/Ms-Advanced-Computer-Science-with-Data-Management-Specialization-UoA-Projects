import kvServerlib as server
import Trie_Structure as trie
import server as srv
import sys

if __name__ == "__main__":
    host, port = server.check_input_data(sys.argv)
    initial_trie_dict = trie.Node(".")
    server_thread = srv.Server(host,port)
    server_thread.initialize_server(initial_trie_dict)