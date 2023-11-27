import os
from collections import defaultdict
import json

"""
count lenths fo 66 of the test set games to choose a development set
"""
structures = ['C151', 'C156', 'C142', 'C6', 'C28', 'C145', 'C150', 'C148', 'C89', 'C54']

current_folder=os.getcwd()

corpus_path = '/home/kate/minecraft_corpus/stats/jsons/test_set_66.json'

try:
    with open(corpus_path, 'r') as f: 
        obj = f.read()
        test_data = json.loads(obj)
except IOError:
    print('cannot open json file ' + corpus_path)

final_list = []
sub_list = []
for game in test_data:
    gold_id = game['id']
    gid = gold_id.split('-')[0]
    len_game = len(game['edus'])
    final_list.append((gold_id, len_game))
    if gid in structures:
        sub_list.append((gold_id, len_game))

fl = sorted(final_list, key=lambda x: x[1])

sl = sorted(sub_list, key=lambda x: x[1])

for f in fl:
    print(f)
print('---------')
print(len(sl))
for s in sl:
    print(s)
