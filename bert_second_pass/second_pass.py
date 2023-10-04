"""
adds info to edus that is necessary for more second pass (Narration) processing.
info: global turn, architect edu index in turn, 1/0 result incoming, edu type
returns only narration relations. 
"""
import os 
import json 
from collections import Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_in/'
save_path = current_folder + '/json_out/'


# games = 'bert_multi_preds_30.json'
games = 'bert_multi_preds_30_katelinear.json'

new_games = 'bert_multi_preds_30_second_pass.json'

gold_test = 'TEST_30_bert.json'

def contains_number(string):
    return any(char.isdigit() for char in string)

def is_nl(edu):
    """
    if every word in alphanumeric
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word):
            nl = 0
            break
    return nl

def format_preds(preds_file):
    """
    if bert output, need to change relations field
    """
    for game in preds_file:
        new_rels = []
        rels = game['pred_relations']
        for rel in rels:
            rel['x'] = int(rel['x'])
            rel['y'] = int(rel['y'])
            new_rels.append(rel)
        game['relations'] = new_rels
    return preds_file

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
    if 'preds' in games:
        jfile = format_preds(jfile)
    for game in jfile:
        rels = game['relations']
        edus = game['edus']
        new_rels = []
        
        #add turn index for arch and global turn info to all edus
        ind_cnt = 0
        global_cnt = 0
        last_speaker = None
        global_index = 0
        for edu in edus:
            edu['global_index'] = global_index
            global_index += 1
            speaker = edu['speaker']
            if speaker == last_speaker:
                edu['turn'] = global_cnt
            else:
                last_speaker = speaker
                global_cnt += 1
                edu['turn'] = global_cnt
            if speaker == 'Architect':
                edu['turn_ind'] = ind_cnt
                ind_cnt += 1
            elif speaker == 'Builder':
                ind_cnt = 0
            #also add type info
            if is_nl(edu['text']):
                edu['type'] = 0
            else:
                edu['type'] = 1
            #add field for incoming result information
            edu['res'] = 0

        #add incoming Result information
        for rel in rels:
            if rel['type'] == 'Result':
                ind = rel['y']
                edus[ind]['res'] = 1
            
            #keep only Narration relations
            if rel['type'] == 'Narration':
                new_rels.append(rel)         
        game['relations'] = new_rels

if 'preds' in games:
    #switch out output narrations with gold narrations
    with open(open_path + gold_test, 'r') as jf:
        goldfile = json.load(jf)
    narr_dict = {}
    for gg in goldfile:
        narr_dict[gg['id']]=[rel for rel in gg['relations'] if rel['type'] == 'Narration']
    gold_rels = []
    for g in jfile:
        g['relations'] = narr_dict[g['id']]
    with open(save_path + new_games, 'w') as outfile:
        json.dump(jfile, outfile)
    print('test json saved')
else:
    with open(save_path + new_games, 'w') as outfile:
        json.dump(jfile, outfile)
    print('train json saved')
