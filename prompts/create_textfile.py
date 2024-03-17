import os
import json
from collections import defaultdict

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

    total_snippets = 0
    total_corrections = 0

    for game in games[:3]:
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
            edu_list = [[edu['speaker'], [], edu['text']] for edu in game['edus']]
            for rel in game['relations']:
                if rel['type'] in ['Narration', 'Correction', 'Continuation', 'Result']: ##!! Just look at Corrections
                    edu_list[rel['y']][1].append([rel['x'], rel['type']])
            for i, item in enumerate(edu_list):
                item_string = str(i) + ' <' + item[0] + '> ' 
                for inc_rel in item[1]:
                    item_string += '$$[' + str(inc_rel[0]) + ',' + inc_rel[1] + ']$$ '
                ##check for NL moves
                if item[0] == 'Builder' and is_nl(item[2]):
                    item_string += decode(item[2])
                else:
                    item_string += item[2]
                item
                text_list.append(item_string)

            #now want to separate by Narrations. 
            narrations_dict = {}
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
            for key in sorted(narrations_dict.keys()):
                snip = narrations_dict[key]
                no_snip = 1
                corr = 0
                for s in snip: 
                    if '|put' in s or '|remove' in s:
                        no_snip = 0
                    if ',Correction' in s:
                        corr = 1
                if no_snip:
                    pass
                elif corr:
                    total_corrections += 1
                    total_snippets += 1
                    prompt_snippets.append('----' + game_id + '_' + str(key) + '_CORRECTION' + '----')
                    for s in snip:
                        if ',Correction' in s:
                            prompt_snippets.append(s)
                        else:
                            if '$$' in s:
                                ss = s.split('$$')
                                new_s = ss[0] + ss[-1]
                                prompt_snippets.append(new_s)
                            else:
                                prompt_snippets.append(s)
                else:
                    total_snippets += 1
                    prompt_snippets.append('----' + game_id + '_' + str(key) + '----')
                    for s in snip:
                        if '$$' in s:
                            ss = s.split('$$')
                            new_s = ss[0] + ss[-1]
                            prompt_snippets.append(new_s)
                        else:
                            prompt_snippets.append(s)
        
            # for t in narrations_list:
            #     print(t)
    print_string = '\n'.join(prompt_snippets)
    with open (current_folder+ '/akshay.txt', 'w') as txt_file:
        txt_file.write(print_string)
    
    print('total snippets : ', total_snippets)
    print('total corrections : ', total_corrections)

