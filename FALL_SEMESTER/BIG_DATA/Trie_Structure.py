import Codes

class Node():
    def __init__(self, letter):
        self.letter = letter # letter of trie node
        self.parent = None # the previous letter
        self.children_vert_ls = [] # the next letters
        self.is_leaf_flag = False # a flag that is true when we are at the end of our word
        self.word = None # whole key string
        self.child_key = [] # the children keys of the top key
        self.node_val = None
        # if root key
        self.root_key_flag = False
        # the nested trie struct
        self.nested_nodes = None # nested vertices

      
def add_new_key(dict, key, root_key_flag):
    """
    With the add_new_key function we add a new key (charachters of the new key).
    We search if letters of the word already exist and if yes we add the rest nodes
    after the the nodes that are already in the structure. 
    """
    current_vert = dict
    for char in key:
        node_exist_flag = False
        for child in current_vert.children_vert_ls:
            if char == child.letter:
                node_exist_flag = True
                current_vert = child
                break
        if node_exist_flag == False:
            new_node = Node(char)
            new_node.parent = current_vert
            if len(current_vert.children_vert_ls) == 0: # if list is empty just append the new node and return
                current_vert.children_vert_ls.append(new_node)
            idx = 0
            for sub_node in current_vert.children_vert_ls:
                while new_node.letter > sub_node.letter:
                    idx += 1
                    break
            current_vert.children_vert_ls.insert(idx, new_node)
            current_vert = new_node
    current_vert.is_leaf_flag = True
    current_vert.root_key_flag = root_key_flag
    current_vert.key = key
    return current_vert

def add_nested_node(nested_node, value_dict):
    """
    With that function we recursively iterate from each nested key-value pair
    of each top level key and with add the nested key-value pairs
    """
    current_vert = nested_node
    if type(value_dict) != type(dict()) or value_dict=={}:
        nested_node.node_val = value_dict
        return Codes.finished
    current_vert.nested_nodes = Node(".")
    for key in value_dict.keys():
        current_vert.child_key.append(key)
        nested_node = add_new_key(current_vert.nested_nodes, key, False)
        add_nested_node(nested_node, value_dict[key])
    return Codes.finished

def add_nested_key_value(trie_struct, value_dict):
    """
    We add the new key and the nested key value pairs. If the top level key already exists
    the function returns. If not it adds the key and the nested key-values
    """
    top_key = list(value_dict.keys())[0]
    key_exists, node = find_key(trie_struct, top_key)
    if key_exists:
        return Codes.finished
    else:
        node = add_new_key(trie_struct, top_key, True)
        add_nested_node(node, value_dict[top_key])
    return Codes.finished

def get_nested_val(node):
    """
    That function recurcively iterates over the trie and the nested key-value pairs
    and returns a dictionary or a value
    """
    if node.node_val != None or node.node_val=={}:
        return node.node_val
    key_vals_nested_dict = {}
    k_nested = node.nested_nodes
    for key in node.child_key:
        _, new_node = find_key(k_nested, key)
        key_vals_nested_dict[key] = get_nested_val(new_node)
    return key_vals_nested_dict

def find_nested_key_value(trie_struct, key_val_ls):
    """
    With that function we search if the key user provided exists as upper level key, and return its values
    if other child keys are provided it returns the value of the last key provided with 
    the get_nested_val function
    """
    _, top_node = find_key(trie_struct, key_val_ls[0])
    if top_node == None:
        return False, None
    if len(key_val_ls) == 1:
        key_vals_nested_dict = get_nested_val(top_node)
        return key_vals_nested_dict != None, key_vals_nested_dict
    elif len(key_val_ls) > 1:
        node = top_node
        for k in key_val_ls[1:]:
            if k in node.child_key:
                _, node = find_key(node.nested_nodes, k)
                if node == None:
                    return False, None
            else:
                return False,None
    key_vals_nested_dict = get_nested_val(node)
    return key_vals_nested_dict != None, key_vals_nested_dict


def find_key(trie_struct, k):
    """
    With that function we find the key provided, in the structure and return
    its value and a flag that if it exists in the struct
    """
    exists_in_trie = False
    current_vert = trie_struct
    vert_value = None
    for ch in k:
        is_char_flag = False
        for child in current_vert.children_vert_ls:
            if ch == child.letter:
                current_vert = child
                is_char_flag = True
                break
        if is_char_flag == False:
            return exists_in_trie, None
    if is_char_flag == True and current_vert.is_leaf_flag == True:
        exists_in_trie = True
        vert_value = current_vert
    return exists_in_trie, vert_value


def delete_key(trie_struct, key):
    """
    With that function we delete the upper level key inside the trie struct
    """
    if_exists, vert_key = find_key(trie_struct,key)
    if if_exists == True:
        vert_key.is_leaf_flag = False
        vert_key.root_key_flag = False
        vert_key.child_key = []
        vert_key.node_val = None
        vert_key.nested_nodes = None
        vert_key.key = None
        vert_tmp = vert_key
        while vert_tmp != None:
            current_vert = vert_tmp
            vert_tmp = vert_tmp.parent
            if len(current_vert.children_vert_ls) == 0:
                if vert_tmp != None and current_vert in vert_tmp.children_vert_ls:
                    vert_tmp.children_vert_ls.remove(current_vert)
                del current_vert
        if_exists, vert_key = find_key(trie_struct, key)
    else:
        return Codes.NOT_FOUND # 404
    return Codes.NO_CONTENT # 204