import os
import json
# from collections import defaultdict

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
    [Builder puts down/picks up a yellow block at X:3 Y:1 Z:0]
    """
    zdict = {'a':'-5', 'e' : '-4', 'i':'-3', 'o':'-2', 'u':'-1', 'p':'0', 
             'q':'1', 'r':'2', 'x': '3', 'y':'4', 'z':'5'}
    xdict = {'b': '-5', 'c' :'-4', 'd' : '-3', 'f' : '-2', 'g' : '-1', 'h':'0', 
             'j':'1', 'k':'2', 'l':'3', 'm':'4', 'n':'5'}
    colors = {'r' :'red', 'b':'blue', 'g':'green', 'o':'orange', 'y':'yellow', 'p':'purple'}
    action = {'0' : 'Builder picks up a', '1': 'Builder puts down a'}
    decoded = []
    for tok in tok_str.split():
        # print(tok)
        new_string = '[' + action[tok[0]] + ' ' + colors[tok[1]] + ' block at X:' +  xdict[tok[2]] + ' Y:' + tok[3] + ' Z:' + zdict[tok[4]] + ']'
        decoded.append(new_string)
    dec_str = '\n'.join(decoded)
    return dec_str

def orig_id(glozz_id):
    """
    takes an id and re-arranges for B-A-C
    """
    glozz = glozz_id.split('-')
    new_id = glozz[1]+'-'+glozz[2]+'-'+glozz[0]
    return new_id

current_folder=os.getcwd()

corpus_path = current_folder + '/COCO_dev_30.json'

text_list = []

with open(corpus_path, 'r') as j:
    jfile = json.load(j)
    games = jfile
    games_list = []

    for game in games:
        # if game['id'] in ['C54-B13-A30']:
            # text_list.append(game['id'])
            print(game['id'])

            #make a list of edus w/ index
            #[[speaker, rels, text]]
            #then go through rels and plant them by index
            # [[speaker, [[0, Ack]], text]]
            #for list in edus list, add to text list :
            # 0. <Speaker> [0 Ack], text
            #see how this looks then figure out how to separate narrations
            edu_list = [[edu['speaker'], [], edu['text']] for edu in game['edus']]
            for rel in game['relations']:
                if rel['type'] in ['Correction']: ##!! Just look at Corrections
                    edu_list[rel['y']][1].append([rel['x'], rel['type']])
            for i, item in enumerate(edu_list):
                rels_str = ''
                for inc_rel in item[1]:
                    rels_str += '[[' + str(inc_rel[0]) + ',' + inc_rel[1] + ']] '
                item_string = str(i) + ' <' + item[0] + '> ' + rels_str
                # item_string = '<' + item[0] + '> ' 
                # for inc_rel in item[1]:
                #     item_string += '[[' + str(inc_rel[0]) + ',' + inc_rel[1] + ']] '
                ##check for NL moves
                if item[0] == 'Builder' and is_nl(item[2]):
                    item_string = str(i) + rels_str
                    item_string += decode(item[2])
                else:
                    item_string += item[2]
                # item
                text_list.append(item_string)

            #now want to separate by Narrations. 
            # narr_no = 0
            # narrations_list = []
            games_list.append(orig_id(game['id']))
            for line in text_list:
                games_list.append(line)
            games_list.append('\n')
            
            #empty text list
            text_list = []
        
            # for t in narrations_list:
            #     print(t)
    print_string = '\n'.join(games_list)
    with open (current_folder+ '/corrections_sample_v2.txt', 'w') as txt_file:
        txt_file.write(print_string)

