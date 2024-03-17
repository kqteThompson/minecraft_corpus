import os
import json
from collections import defaultdict

"""
look at first instructions to get an idea for templates
"""

def is_nl(edu):
    """
    if every word in alphanumeric and has len 5
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word) or len(word) < 5:
            nl = 0
            break
    return nl

def contains_number(string):
    return any(char.isdigit() for char in string)

def decode(tok_str):
    """
    takes a list bert tokens and changes them back to coordinates.
    """
    zdict = {'a':'-5', 'e' : '-4', 'i':'-3', 'o':'-2', 'u':'-1', 'p':'0', 
             'q':'1', 'r':'2', 'x': '3', 'y':'4', 'z':'5'}
    xdict = {'b': '-5', 'c' :'-4', 'd' : '-3', 'f' : '-2', 'g' : '-1', 'h':'0', 
             'j':'1', 'k':'2', 'l':'3', 'm':'4', 'n':'5'}
    colors = {'r' :'red', 'b':'blue', 'g':'green', 'o':'orange', 'y':'yellow', 'p':'purple'}
    action = {'0' : 'remove', '1': 'put'}
    decoded = []
    for tok in tok_str.split():
        # print(tok)
        new_string = action[tok[0]] + ' ' + colors[tok[1]] + ' X:' +  xdict[tok[2]] + ' Y:' + tok[3] + ' Z:' + zdict[tok[4]]
        decoded.append(new_string)
    dec_str = '|'.join(decoded)
    full_dec = '|'+ dec_str
    return full_dec

current_folder=os.getcwd()

corpus_path = current_folder + '/DEV_32_bert.json'

with open(corpus_path, 'r') as j:
    jfile = json.load(j)
    games = jfile


    instructions = []

    for game in games:
            ##STEP 1
            print(game['id'])
            game_id = game['id']
            text_list = []
            #make a list of edus w/ index
            #[[speaker, rels, text]]
            #then go through rels and plant them by index
            # [[speaker, [[0, Ack]], text]]
            #for list in edus list, add to text list :
            # 0. <Speaker> [0 Ack], text
            #see how this looks then figure out how to separate narrations
            edu_list = [[edu['speaker'], edu['text'],[]] for edu in game['edus']]
            for rel in game['relations']:
                # if rel['type'] in ['Narration', 'Correction', 'Continuation', 'Result']: ##!! Just look at Corrections
                    edu_list[rel['y']][2].append([rel['x'], rel['type']])
            for i, item in enumerate(edu_list):
                item_string = str(i) + ' <' + item[0] + '> ' 
                ##check for NL moves
                if item[0] == 'Builder' and is_nl(item[1]):
                    item_string += decode(item[1])
                else:
                    item_string += item[1]
                ##add relations
                if len(item[2]) > 0:
                    item_string += '$$'
                for inc_rel in item[2]:
                    item_string += '[' + str(inc_rel[0]) + ',' + inc_rel[1] + '] '
                text_list.append(item_string)

            #now want to separate by Narrations. 
            narrations_dict = {} #json2
            narr_no = 0
            # narrations_list = []
            narrations_list = []
            for line in text_list:
                if ',Narration' in line and ',Result' in line:
                    narrations_dict[narr_no] = narrations_list
                    narr_no += 1
                    narrations_list = []
                    narrations_list.append(line)
                else:
                    narrations_list.append(line)
            
            # print(narrations_dict.keys())
            # STEP 2: for each narration, find first instruction.
            
            for key in sorted(narrations_dict.keys()):
                snip = narrations_dict[key]
                for s in snip: 
                    if '|put' in s or '|remove' in s:
                        instructions.append('\n')
                        break
                    else:
                        instructions.append(s)
                   
              
    """
    NB:
    For this first pass, we take only correction snippets that have 2 move turns and 
    2 corrections, and non-correction snippets that have 2 move turns, or one move turn 
    then we add he first move turn of the next consecutive snippet if it is not a
    correction
    """
    # ##to check the intermediate json
    # print(len(filtered_snippets)) 
    # print(len([i for i in filtered_snippets if i['corr'] == 1]))                     
    # with open(current_folder+ '/akshay.json', 'w') as outfile:
    #     json.dump(filtered_snippets, outfile)




    print_string = '\n'.join(instructions)
    with open (current_folder+ '/instruct_test.txt', 'w') as txt_file:
        txt_file.write(print_string)
    

