import os
import json
from collections import defaultdict

"""
overall goal: test whether a model can tell the difference between two sets of moves that are corrections
of one another or not.

takes a json of annotated games
step 1: transform games json1 into snippets at Narr/Result json2
step 2: json2 - json 3 keep snippet that have correction triangles and snippets that 
    a. have no corrections b. have moves c. have a next snippet that is not a correction that has moves
    UNLESS the snippet has more than one set of moves.
step 3: change json3 to snippets list, with equal numbers corrections and non corrections
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

corpus_path = current_folder + '/TRAIN_303_bert.json'

with open(corpus_path, 'r') as j:
    jfile = json.load(j)
    games = jfile
    prompt_snippets = []
    filtered_snippets = [] ##a list of jsons

    for game in games:
            ##STEP 1
        # if game['id'] in ['C120-B53-A4', 'C87-B25-A10', 'C49-B52-A27', 'C50-B15-A27', 'C157-B11-A7']:
            # text_list.append(game['id'])
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
                if rel['type'] in ['Narration', 'Correction', 'Continuation', 'Result']: ##!! Just look at Corrections
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
            #STEP 2: remove anything that is not correction and remove snippets that do not contain moves
            
            hold = {'key': 'None', 'snip': 'None'}
            for key in sorted(narrations_dict.keys()):
                snip = narrations_dict[key]
                num_moves = 0
                corr = 0
                corr_triangle = 0
                for s in snip: 
                    if '|put' in s or '|remove' in s:
                        num_moves += 1
                    if ',Correction' in s:
                        corr += 1
                    if ',Correction' in s and ',Result' in s:
                        corr_triangle += 1
                if num_moves == 0 or (corr and not corr_triangle):
                    pass
                else:
                    #if correction, add it
                    #if not correction > 1 moves, add it
                    #if not correction == 1 moves, check next snippet 
                    if corr_triangle == 1 and num_moves == 2 and corr < 3:
                        snippet = {}
                        snippet['id'] = game_id + '_' + str(key)
                        snippet['corr'] = 1
                        snippet['text'] = snip
                        filtered_snippets.append(snippet)
                    else:
                        if num_moves > 1 and corr == 0:
                            snippet = {}
                            snippet['id'] = game_id + '_' + str(key)
                            snippet['corr'] = 0
                            snippet['text'] = snip
                            filtered_snippets.append(snippet)
                            #check for a previous unfiltered snippet
                            if hold['key'] != 'None' and key == hold['key'] + 1:
                                snippet = {}
                                snippet['id'] = game_id + '_' + str(hold['key'])
                                snippet['corr'] = 0
                                add_snip = []   
                                for s in snip:
                                    if '|put' in s or '|remove' in s:
                                        add_snip.append(s)
                                        break
                                    else:
                                        add_snip.append(s)
                                hold['snip'].extend(add_snip)
                                snippet['text'] = hold['snip']
                                snippet['ext'] = 1
                                filtered_snippets.append(snippet)
                                #put first move on snip and add
                                #clear hold dict
                                hold = {'key': 'None', 'snip': 'None'}
                        else:
                            #hold for next moves
                            pass
                            if num_moves == 1 and corr == 0:
                                #put in hold
                                hold['key'] = key
                                hold['snip'] = snip
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


    #transform the json into a printable string
    correction_count = 0 ##don't take more than 129 corrections
    # number gotten from counts in json above
    total_snippets = 0
    for snip in filtered_snippets:
        if snip['corr'] == 1:
            if correction_count > 129:
                pass
            else:
                prompt_snippets.append(snip['id'] + '_CORRECTION')
                correction_count += 1
                total_snippets += 1
        else:
            prompt_snippets.append(snip['id'])
            total_snippets += 1
        for line in snip['text']:
            if '$$' in line and ',Correction' not in line:
                newline = line.split('$$')[0]
                prompt_snippets.append(newline)
            else:
                prompt_snippets.append(line)
        prompt_snippets.append('\n')

    print(total_snippets, " total snippets")
    print(correction_count - 1, " correction snippets")
    print_string = '\n'.join(prompt_snippets)
    with open (current_folder+ '/akshay.txt', 'w') as txt_file:
        txt_file.write(print_string)
    

