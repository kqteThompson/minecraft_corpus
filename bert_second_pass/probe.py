"""
changes nonlinguistic moves -- pick to place --0 to 1.  
"""
import os 
import json 
from collections import Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_in/'
save_path = current_folder + '/json_out/'

# games = 'bert_multi_preds_30_katelinear.json'
games = 'TEST_30_bert.json'

# new_games = 'bert_multi_preds_30_second_pass.json'
new_games = 'TEST_30_bert_probe.json'


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

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
    for game in jfile[:1]:
        edus = game['edus']
        for edu in edus:
            if is_nl(edu['text']):
                new_text = []
                for str in edu['text'].split(' '):
                    # print(str, len(str))
                    if len(str) > 0:
                        newst = str.replace(str[0], '1')
                        new_text.append(newst)
                    # new_text.append(' ')
                    new_str = ' '.join(new_text)
                edu['text'] = new_str

    with open(save_path + new_games, 'w') as outfile:
        json.dump(jfile, outfile)
    print('train json saved')
