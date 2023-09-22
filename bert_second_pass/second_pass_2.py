"""
Takes a json file second pass games and removes all 
NL elements/Builder utterances
But also re-indexes the narration links afterwards
"""
import os 
import json 
from collections import Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_out/'

save_path = current_folder + '/json_out/'

# games = 'bert_multi_preds_30.json'
games = 'multi_preds_30_second_pass.json'

new_games = 'multi_preds_30_second_pass_archonly.json'


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
    for game in jfile:
        new_edus = []
        edus = game['edus']
        cnt = 0
        #this is for removing only NL moves
        # for edu in edus:
        #     if edu['type'] == 1:
        #         edu['tmp_index'] = cnt
        #         new_edus.append(edu)
        #     cnt += 1
        for edu in edus:
            if edu['speaker'] == 'Architect':
                edu['tmp_index'] = cnt
                new_edus.append(edu)
            cnt += 1

        index_dict = {}
        #assuming that the edus are indexed at 0
        for i, edu in enumerate(new_edus):
            index_dict[edu['tmp_index']] = i
        rels = game['relations'] 
        new_rels = []
        try:
            for rel in rels:
                new_rel = {}
                new_rel['x'] = index_dict[rel['x']]
                new_rel['y'] = index_dict[rel['y']]
                new_rel['type'] = rel['type']
                new_rels.append(new_rel)
        except KeyError:
            print('Key error in game {}'.format(game['id']))
            continue
            
        
        game['edus'] = new_edus
        game['relations'] = new_rels

with open(save_path + new_games, 'w') as outfile:
    json.dump(jfile, outfile)
print('test json saved')

