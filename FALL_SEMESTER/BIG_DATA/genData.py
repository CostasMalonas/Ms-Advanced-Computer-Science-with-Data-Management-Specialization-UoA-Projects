import sys 
import genDatalib as dl
import json
import os



argument_list = sys.argv
file_name, num_lines, max_nesting, max_str_len, key_vals_per_lvl = dl.check_input_data(argument_list)


def print_dict(d):
    for k, v in d.items():
        print(k,":",v)

final = {}
top_lvl_key = "key"
for i in range(num_lines):
    final[top_lvl_key+str(i+1)] = dl.main(max_nesting, key_vals_per_lvl, max_str_len, file_name)

with open("dataToIndex.txt", 'w') as f: 
    for key, value in final.items(): 
        f.write(("'%s' : %s\n" % (key, value)).replace("'", "\"")) # write lines in file in json format

