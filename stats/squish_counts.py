import os
import json
import pickle
from collections import defaultdict

"""
uses the squish data recorded in a pickle in the 'flatten' phase
finds the edus and relation types involved in the squishing
outputs a text file 

squishes pickle is a default dict with game ids as keys, and a list of (source, target) 
edu pairs as values
"""
current_folder=os.getcwd()

pickle_path = '/home/kate/minecraft_corpus/flatten/squish.pkl'

json_path = '/home/kate/minecraft_corpus/glozz_to_json/json_output/SILVER_2023-06-12.json'

with open(pickle_path, 'rb') as handle:
    squishes = pickle.load(handle)

with open(json_path, 'r') as j:
    jfile = json.load(j)
    games = jfile

count_list = []
print_list = []
for game in games:
    if game['game_id'] in squishes.keys():
        count = 0
        print(game['game_id'])
        print(squishes[game['game_id']])
        print_list.append('--------------------' + game['game_id'] + '-----------------------')
        game_rels = defaultdict(list)
        for rel in game['relations']:
            game_rels[rel['x_id']].append((rel['y_id'], rel['type']))
        edus = {edu['unit_id']: edu['Speaker'] + ' : ' + edu['text'] for edu in game['edus']}
        for elem in squishes[game['game_id']]:
            targets = game_rels[elem[0]]
            for t in targets:
                if t[0] == elem[1]:
                    try:
                        print_list.append(edus[t[0]])
                        print_list.append(t[1])
                        count += 1
                        print_list.append('-----------------------')
                    except KeyError:
                        print_list.append('CDU target: {}'.format(t[0]))
                        # print('key error skipping edu {}'.format(t[0]))
        print_list.append('-------' + str(count) + '   danglers squished. ')
        count_list.append((game['game_id'], str(count)))
        

print_string = '\n'.join(print_list)
    

with open (current_folder+ '/squish_info.txt', 'w') as txt_file:
    txt_file.write(print_string)

print('squish information saved')
for c in count_list:
    print(c[0], c[1])
