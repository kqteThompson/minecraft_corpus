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

merge = ['TEST_30_bert.json', 'TRAIN_314_bert.json']

new_file = 'MERGED_344.json'

countdict = Counter()

final_list = []
for file in merge:
    with open(open_path + file, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            final_list.append(game)

print('final games : {}'.format(len(final_list)))

with open(open_path + new_file, 'w') as outfile:
    json.dump(jfile, outfile)

print('json saved')
