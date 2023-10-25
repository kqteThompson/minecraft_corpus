
import os
import json
import sys
"""
use this script as a way to locate problematic relations
"""

current_dir = os.getcwd()
##try to open json file and check turns 
gold_annotations = '2023-10-FLAT.json'
gold = '/home/kate/minecraft_corpus/glozz_to_json/json_output/SILVER_2023-10-13.json'
# gold_annotations = 'TEST_30_bert.json'
# gold_annotations = 'TRAIN_314_bert.json'



# gold = current_dir + '/jsons/' + gold_annotations

try:
    with open(gold, 'r') as f: 
        obj = f.read()
        gold_data = json.loads(obj)
except IOError:
    print('cannot open json file ' + gold)

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
        if not contains_number(word) or not len(word) == 5:
            nl = 0
            break
    return nl

eeus = 0
for game in gold_data:
    # id = game['id']
    edus = game['edus']
    for edu in edus:
        if edu['Speaker'] == 'System':
            eeus += 1

print(eeus)





    # rels = game['relations']
    # for rel in rels:
    #     if rel['type'] == 'Background':
    #         target = rel['y']
    #         edu = game['edus'][target]
    #         print('game id: {}, speaker: {}, text: {}'.format(id, edu['speaker'], edu['text']))

    #         print('-----------------------')

# #find bad backwards links
# sys.stdout = open('bad_backwards.txt', 'w')
# count = 1
# for game in gold_data:
#     id = game['id']
#     rels = game['relations']
#     for rel in rels:
#         if rel['type'] not in ['Comment', 'Conditional']:
#             if rel['y'] < rel['x']:
#                 edu = game['edus'][rel['y']]
#                 print('{}. game {}, rel type {}, speaker: {}, text: {} '.format(count, id, rel['type'], edu['speaker'], edu['text']))
#                 print('X: {}'.format(game['edus'][rel['x']]))
#                 count += 1
#                 print('-----------------------')
# sys.stdout.close()


# # find narrations that are not NL-NL
# for game in gold_data:
#     id = game['id']
#     edus = game['edus']
    
#     edu_types = []
#     for edu in edus:
#         if edu['speaker'] == 'Builder' and is_nl(edu['text']):
#             edu_types.append(0)
#         else:
#             edu_types.append(1)
#     for rel in game['relations']:
#         if rel['type'] == 'Narration':
#             if edu_types[rel['x']] == 0 or edu_types[rel['y']] == 0:
#                 print('{} game,  NL Narration edu'.format(id))
#                 print('X : {}'.format(edus[rel['x']]))
#                 print('Y : {}'.format(edus[rel['y']]))
#                 print('-----------------------------------')

# find narrations that are not NL-NL

# for game in gold_data:
#     id = game['id']
  
#     # edus = game['edus']
    
#     # edu_types = []
#     # for edu in edus:
#     #     if edu['speaker'] == 'Builder' and is_nl(edu['text']):
#     #         edu_types.append(0)
#     #     else:
#     #         edu_types.append(1)
#     rel_counts = 0
#     for rel in game['relations']:
#     #     # if rel['type'] == 'Clarification_question':
#     #     #     if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 0:
#     #     #         print('{} game,  L-NL CLARIF edu'.format(id))
#     #     #         print('X : {}'.format(edus[rel['x']]))
#     #     #         print('Y : {}'.format(edus[rel['y']]))
#     #     #         print('-----------------------------------')
#     #     # if rel['type'] == 'Question-answer_pair':
#     #     #     if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 0:
#     #     #         print('{} game,   NL-NL QAP edu'.format(id))
#     #     #         print('X : {}'.format(edus[rel['x']]))
#     #     #         print('Y : {}'.format(edus[rel['y']]))
#     #     #         print('-----------------------------------')
#     #     # if rel['type'] == 'Question-answer_pair':
#     #     #     if edu_types[rel['x']] == 0 and edu_types[rel['y']] == 1:
#     #     #         print('{} game,  L-NL QAP edu'.format(id))
#     #     #         print('X : {}'.format(edus[rel['x']]))
#     #     #         print('Y : {}'.format(edus[rel['y']]))
#     #     #         print('-----------------------------------')
#         # if rel['type'] == 'Correction':
#         #     if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 0:
#         #         print('{} game,  L-NL CORRECTION edu'.format(id))
#         #         print('X : {}'.format(edus[rel['x']]))
#         #         print('Y : {}'.format(edus[rel['y']]))
#         #         print('------------------------------------')
#         if rel['type'] == 'Correction':
#             rel_counts += 1
#     if rel_counts > 0:
#         print('game {} has {} corrections'.format(id, rel_counts))
    
