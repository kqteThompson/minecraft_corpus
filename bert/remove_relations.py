"""
Takes a json file of ANNOTATED games that formatted for BERT and removes
indicated relation types
"""
import os 
import json 
from collections import Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_out/'

json_files = os.listdir(open_path)

remove = ['Narration', 'Correction']

games = 'TEST_30_bert.json'

new_file = 'TEST_30_minus_narr-corr.json'

countdict = Counter()

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
    for game in jfile:
        new_rels = []
        for rel in game['relations']:
            if rel['type'] in remove:
                countdict[rel['type']] += 1
            else:
                new_rels.append(rel)
        game['relations'] = new_rels

for item in [i for i in countdict.items()]:
    print('{} {} relations removed'.format(item[1], item[0]))

with open(open_path + new_file, 'w') as outfile:
    json.dump(jfile, outfile)

print('json saved')
