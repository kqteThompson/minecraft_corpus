
import os
import json
import sys
from collections import defaultdict
"""
use this script as a way to locate problematic relations
"""

current_dir = os.getcwd()
##try to open json file and check turns 
annotations = 'MERGED_536.json'
gold = '/home/kate/minecraft_corpus/glozz_to_json/json_output/SILVER_2023-10-13.json'
# gold_annotations = 'TEST_30_bert.json'
# gold_annotations = 'TRAIN_314_bert.json'



gold = current_dir + '/jsons/' + annotations

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

# #for each game count number of relations
# length_counts = []
# for game in gold_data:
#     id = game['id']
#     rels = game['relations']
#     for rel in rels:
#         if rel['type'] in ['Narration']:
#             length = abs(rel['y'] - rel['x'])
#             length_counts.append(length)
# print('num rels: ', len(length_counts))
# print('avg len: ', sum(length_counts)/len(length_counts))

#for each game, count edus, etc.
# game_counts = []
# for game in gold_data:
#     id = game['id']
#     rels = game['relations']
#     count = 0
#     for rel in rels:
#         count += 1
#     game_counts.append(count)
# print('num rels: ', len(game_counts))
# print('max len :', max(game_counts))
# print('avg len: ', sum(game_counts)/len(game_counts))

eeu_counts = []
edu_counts = []
for game in gold_data:
    id = game['id']
    edus = game['edus']
    edu_count = 0
    eeu_count = 0
    for edu in edus:
        if is_nl(edu['text']):
            eeu_count += 1
        else:
            edu_count += 1
    edu_counts.append(edu_count)
    eeu_counts.append(eeu_count)

print('total eeus: ', sum(eeu_counts))
print('total edus: ', sum(edu_counts))
print('max eeus in a game :', max(eeu_counts))
print('max edus in a game :', max(edu_counts))
print('avg eeus: ', sum(eeu_counts)/len(eeu_counts))
print('avg edus: ', sum(edu_counts)/len(edu_counts))


turn_counts = []
for game in gold_data:
    id = game['id']
    edus = game['edus']
    last_speaker = 'None'
    turns = 0
    for edu in edus:
        if not is_nl(edu['text']):
            if edu['speaker'] != last_speaker:
                turns += 1
                last_speaker = edu['speaker']
    turn_counts.append(turns)

print('total turns: ', sum(turn_counts))
print('max turns in a game :', max(turn_counts))
print('avg turns: ', sum(turn_counts)/len(turn_counts))

# eeu_counts = []
# for game in gold_data:
#     id = game['id']
#     edus = game['edus']
#     eeu_count = 0
#     for edu in edus:
#         if is_nl(edu['text']):
#             moves = edu['text'].split(' ')
#             # num_moves = len(moves)
#             eeu_count += len(moves)
#     eeu_counts.append(eeu_count)

# print('sum total eeus :', sum(eeu_counts))
# print('max eeus in a game :', max(eeu_counts))
# print('avg eeus: ', sum(eeu_counts)/len(eeu_counts))

#distinguish narrations
#short from long narrations
# short_narr = []
# long_narr = []
# for game in gold_data:
#     edu_list = [[i,defaultdict(list)] for i, edu in enumerate(game['edus'])]
#     for rel in game['relations']:
#         if rel['type'] in ['Narration', 'Result']:
#             edu_list[rel['y']][1][rel['type']].append(rel['x'])
#     # print(edu_list)
#     for l in edu_list:
#         if 'Narration' in l[1].keys() and 'Result' in l[1].keys():
#             if len(l[1]['Narration']) > 1:
#                 print('yes')
#                 #figure out how we are going to
#                 long_one = max(l[1]['Narration'])
#                 short_one = max(l[1]['Narration'])
#                 long_length = abs(l[0] - long_one)
#                 long_narr.append(length)
#                 short_length = abs(l[0] - short_one)
#                 short_narr.append(length)
#             else:
#                 length = abs(l[0] - l[1]['Narration'][0])
#                 long_narr.append(length)
#         elif 'Narration' in l[1].keys() and 'Result' not in l[1].keys():
#             for elem in l[1]['Narration']:
#                 length = abs(l[0] - elem)
#                 # short_narr.append(length)

# # print(long_narr)
# # print(short_narr)
# print('total long narr: ', len(long_narr))
# print('max len long narr :', max(long_narr))
# print('avg len long narr: ', sum(long_narr)/len(long_narr))
# print('total short narr: ', len(short_narr))
# print('max len short narr :', max(short_narr))
# print('avg len short narr: ', sum(short_narr)/len(short_narr))
    
    # for i, item in enumerate(edu_list):
    #     item_string = str(i) + ' <' + item[0] + '> ' 
    #     for inc_rel in item[2]:
    #         item_string += '[' + str(inc_rel[0]) + ',' + inc_rel[1] + '] '
    #     text_list.append(item_string)


# count = 1
# for game in gold_data:
#     id = game['id']
#     rels = game['relations']
#     for rel in rels:
#         if rel['type'] in ['Background', 'Parallel']:
#             target = rel['y']
#             edu = game['edus'][target]
#             print('{}. relation: {} game id: {}, speaker: {}, text: {}'.format(count, rel['type'], id, edu['speaker'], edu['text']))
#             print('-----------------------')

# #find bad backwards links
# # sys.stdout = open('bad_backwards.txt', 'w')
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
# # sys.stdout.close()


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
#         if rel['type'] in ['Correction']:
#             if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 0:
#                 print('{} game,  {} edu'.format(id, rel['type']))
#                 print('X : {}'.format(edus[rel['x']]))
#                 print('Y : {}'.format(edus[rel['y']]))
#                 print('-----------------------------------')

# find narrations that are not NL-NL

# for game in gold_data:
#     id = game['id']
  
#     edus = game['edus']
    
#     edu_types = []
#     for edu in edus:
#         if edu['speaker'] == 'Builder' and is_nl(edu['text']):
#             edu_types.append(0)
#         else:
#             edu_types.append(1)
#     rel_counts = 0
#     for rel in game['relations']:
#         if rel['type'] == 'Question-answer_pair':
#             if edu_types[rel['x']] == 0 and edu_types[rel['y']] == 1:
#                 print('{} game,  NL-Lin QAP edu'.format(id))
#                 print('X : {}'.format(edus[rel['x']]))
#                 print('Y : {}'.format(edus[rel['y']]))
#                 print('-----------------------------------')
    #     if rel['type'] == 'Narration':
    #         if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 0:
    #             print('{} game,   L-NL NAR edu'.format(id))
    #             print('X : {}'.format(edus[rel['x']]))
    #             print('Y : {}'.format(edus[rel['y']]))
    #             print('-----------------------------------')
    #     if rel['type'] == 'Narration':
    #         if edu_types[rel['x']] == 0 and edu_types[rel['y']] == 1:
    #             print('{} game,  NL-L NAR edu'.format(id))
    #             print('X : {}'.format(edus[rel['x']]))
    #             print('Y : {}'.format(edus[rel['y']]))
    #             print('-----------------------------------')
    #     if rel['type'] == 'Sequence':
    #         if edu_types[rel['x']] == 1 and edu_types[rel['y']] == 1:
    #             print('{} game,  L-L SEQ edu'.format(id))
    #             print('X : {}'.format(edus[rel['x']]))
    #             print('Y : {}'.format(edus[rel['y']]))
    #             print('------------------------------------')
    #     if rel['type'] == 'Sequence':
    #         if edu_types[rel['x']] == 0 and edu_types[rel['y']] == 0:
    #             print('{} game,  NL-NL SEQ edu'.format(id))
    #             print('X : {}'.format(edus[rel['x']]))
    #             print('Y : {}'.format(edus[rel['y']]))
    #             print('-----------------------------------')
    #     if rel['type'] == 'Correction':
    #         rel_counts += 1
    # if rel_counts > 0:
    #     print('game {} has {} corrections'.format(id, rel_counts))
    
