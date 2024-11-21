import random
from faker import Faker
import sys
import os

temp_ls = []
temp = []
max_depth = 0
max_key_val_per_lvl = 0
rand_max_key_val_per_lvl = 0 
rand_max_depth = 0 
loops = 0
file_name = ""
lines = []
max_str_len = 0


def check_input_data(argument_list):
    if argument_list[1] != '-k':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif not os.path.exists(argument_list[2]):
        print('KEY FILE NOT EXIST')
        sys.exit()
    elif argument_list[3] != '-n':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif (not argument_list[4].isnumeric()) or (int(argument_list[4]) < 0):
        print("YOU DIDN'T TYPE NUMBER OR NUMBER < 0")
        sys.exit()
    elif argument_list[5] != '-d':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif (not argument_list[6].isnumeric()) or (int(argument_list[6]) < 0):
        print("YOU DIDN'T TYPE NUMBER OR NUMBER < 0")
        sys.exit()
    elif argument_list[7] != '-l':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif (not argument_list[8].isnumeric()) or (int(argument_list[8]) < 0):
        print("YOU DIDN'T TYPE NUMBER OR NUMBER < 0")
        sys.exit()
    elif argument_list[9] != '-m':
        print('WRONG INPUT FORMAT')
        sys.exit()
    elif (not argument_list[10].isnumeric()) or (int(argument_list[10]) < 0):
        print("YOU DIDN'T TYPE NUMBER OR NUMBER < 0")
        sys.exit()
    else:
        return argument_list[2], int(argument_list[4]), int(argument_list[6]), int(argument_list[8]), int(argument_list[10])


def create_fake_values(rand_key):
    # maybe i ll put more keys numerical 
    fake = Faker()
    if rand_key[1] == "string":
        return fake.pystr(min_chars = 1, max_chars= max_str_len)
    elif rand_key[0] == "age":
        return random.randint(1,100)
    elif rand_key[0] == "height":
        return float("%.2f"%random.uniform(0.3, 3.0))
    elif rand_key[0] == "salary":
        return float("%.2f"%random.uniform(700.0, 3000000000.99))
    elif rand_key[1] == "int":
        return random.randint(0,30)
    elif rand_key[0] == "married":
        return random.choice(["Yes", "No"])


def read_from_keyFile(filename):
    with open(filename) as f:
        lines = [line.rstrip().split() for line in f]
    return lines




def create_list_recursively(temp_ls, max_depth, loops):
    if max_depth == 0 and loops != 0:
        rand_line = random.choice(lines)
        #rand_key = random.choice(lines)[0]
        temp_ls.append(rand_line[0]) # take the key
        fake_value = create_fake_values(rand_line)
        temp_ls.append(fake_value)
        return temp[0]   
    elif max_depth == 0:
        if loops == 0:
            rand_line = random.choice(lines)
            #rand_key = random.choice(lines)[0]
            temp_ls.append(rand_line[0])
            fake_value = create_fake_values(rand_line[0])
            temp_ls.append(fake_value)
            return temp_ls
    else:
        loops += 1
        temp_ls.append(random.choice(lines)[0])
        temp_ls.append([])
        max_depth -= 1 
        temp.append(temp_ls)
        return create_list_recursively(temp_ls[-1], max_depth, loops)

#new_ls = create_list_recursively(temp_ls, max_depth, loops)

def create_row():
    # Create each key-value pair for each row  
    row = []
    for i in range(rand_max_key_val_per_lvl):
        try:
            random_key = random.choice(lines)[0]
            if random_key not in temp:
                row.append(random_key)
                rand_max_depth = random.randint(0, max_depth)
                val_ls = create_list_recursively(temp_ls, rand_max_depth, loops)
                row.append(val_ls)
        except:
            continue
    return row

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def nested_pairs2dict(pairs):
    d = {}
    for k, v in pairwise(pairs):
        if isinstance(v, list): # assumes v is also list of pairs
           v = nested_pairs2dict(v)
        d[k] = v
    return d

def replace_none(test_dict): 
  
    # checking for dictionary and replacing if None 
    if isinstance(test_dict, dict): 
        
        for key in test_dict: 
            if test_dict[key] is None: 
                test_dict[key] = dict() 
            else: 
                replace_none(test_dict[key]) 
  
    # checking for list, and testing for each value 
    elif isinstance(test_dict, dict): 
        for val in test_dict: 
            replace_none(val) 

# to be deleted in later version
def main(max_nesting=3, key_vals_per_lvl=2, str_len_max=4,file="keyFile.txt"):
    global temp_ls
    global temp
    global max_depth
    global max_key_val_per_lvl
    global rand_max_key_val_per_lvl
    global rand_max_depth
    global file_name
    global lines
    global max_str_len
    file_name = file 
    temp_ls = []
    temp = []
    max_depth = max_nesting
    max_key_val_per_lvl = key_vals_per_lvl
    rand_max_depth = random.randint(0, max_depth)
    rand_max_key_val_per_lvl = random.randint(0, max_key_val_per_lvl)
    max_str_len = str_len_max
    lines = read_from_keyFile(file_name)
    create_row() # it creates a row and it storing it to the global variable temp_ls
    temp_ls = nested_pairs2dict(temp_ls)
    replace_none(temp_ls)
    return temp_ls


