import json
import Codes
import Trie_Structure as trie
import sys
import operator
import math

def check_input_data(argument_list):
    if argument_list[1] != '-a':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif (not argument_list[2].split('.')[0].isnumeric()) or (not argument_list[2].split('.')[1].isnumeric()) \
        or (not argument_list[2].split('.')[2].isnumeric()) or (not argument_list[2].split('.')[3].isnumeric()):
        print('WRONG HOST FORMAT')
        sys.exit()
    elif argument_list[3] != '-p':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif not argument_list[4].isnumeric():
        print('WRONG HOST FORMAT')
        sys.exit()
    else:
        return argument_list[2], int(argument_list[4])

def prepare_data(data):
    x1, x2 = data.split(":", 1) # split only 1 time at the :
    x1 = x1.strip()
    x1 = x1.strip("\"")
    x2 = x2.strip()
    return x1, x2

def create_data_dict(data):
    row_dict = {}
    top_key, top_val = tuple(map(prepare_data, [data]))[0]
    row_dict[top_key] = json.loads(top_val)
    return row_dict


def PUT(row, trie_data):
    nested_dict_to_trie = create_data_dict(row)
    trie.add_nested_key_value(trie_data, nested_dict_to_trie) 

def DELETE(key, trie_data):
    if trie.delete_key(trie_data, key) == Codes.NO_CONTENT:
        return Codes.SUCCESS
    return Codes.NOT_FOUND


def GET(data, trie_data):
    found, results_dict = trie.find_nested_key_value(trie_data, [data])
    # if found:
    #     return f"{data} : {str(results_dict)[:-len(str(results_dict))]}"
    # return " "
    if found:
        return f"{data} : {results_dict}"
    return " "

def QUERY(data, trie_data):
    trie_key = list(map(str.strip, data.split(".")))
    found, results_dict = trie.find_nested_key_value(trie_data, trie_key)
    if found:
       return f"{'.'.join(trie_key)} : {results_dict}"
    return " "

def COMPUTE(data, trie_data):
    
    split_in_func = list(map(str.strip, data.split(" ", 1))) # take the function and the rest of query
    func = split_in_func[0] # e.g 2+x    
    rest_command = split_in_func[1].replace("WHERE", "").strip() # e.g WHERE x = QUERY key1.examp --> x = QUERY key1.examp
        
    if "AND" in rest_command:
        commands = list(map(str.strip, rest_command.split("AND"))) #e.g x = QUERY key1.examp, y = QUERY key1.examp ...
        for com in commands:
            op_and_query = list(map(str.strip, com.split("="))) # ["x", "QUERY key1.examp, y = QUERY key1.examp"]
            keys_of_query = list(map(str.strip, op_and_query[1].split()))[1] # key1.examp
            keys_of_query = list(map(str.strip, keys_of_query.split(".")))
            found, result = trie.find_nested_key_value(trie_data, keys_of_query) # result
            #op_dict[op_and_query[0]] = result # op_dict["x"] = 5
            func = func.replace(op_and_query[0], str(result))
    else:
        commands = list(map(str.strip, rest_command.split("="))) # [x, "QUERY key1.examp"]
        # with open("commands.txt", 'w') as f:
        #     f.write(str(commands))
        keys_of_query = list(map(str.strip, commands[1].split()))[1]
        keys_of_query = list(map(str.strip, keys_of_query.split(".")))
        found, result = trie.find_nested_key_value(trie_data, keys_of_query)
        #op_dict[commands[0]] = result
        func = func.replace(commands[0], str(result))
        # with open("func_before.txt", 'w') as f:
        #     f.write(func)

    if "log" in func:
        func = func.replace("log", "math.log")
    if "tan" in func:
        func = func.replace("tan", "math.tan")
    if "sin" in func:
        func = func.replace("sin", "math.sin")
    if "cos" in func:
        func = func.replace("cos", "math.cos")
    with open("func_end.txt", 'w') as f:
        f.write(func)
    if found:
       return f"{func} : {eval(func)}"
    return " "
   