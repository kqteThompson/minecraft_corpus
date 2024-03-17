import os
import json
from sklearn.metrics import precision_recall_fscore_support

"""
evaluate performance of the three models on correction triangle prediction.
validation set is from 301 to 330 *300 since 0 index
First count...how many correctly identified as correction or not correction

"""

current_folder=os.getcwd()


llama_7b = 'llama_7b_mc_output.txt'
llama_13b = 'llama_13b_mc_output.txt'
mistral = 'mistral_7b_mc_output.txt'

gold = 'minecraft-corrections.jsonl'


gold_snips = []
with open(current_folder + '/' + gold) as f:
    for line in f:
        gold_snips.append(json.loads(line))
gold_snips = [g['CT'] for g in gold_snips[300:]]
# print(gold_snips)
quick_snips = []
for g in gold_snips:
    if len(g) == 0:
        quick_snips.append(0)
        # print('0 : ', g)
    else:
        quick_snips.append(1)
        # print('1 :', g)
#remove 3 because not present in llama_13b
short_snips = quick_snips[:2]
short_snips.extend(quick_snips[3:])
# print(short_snips)

for output in [llama_7b, mistral]:
    #open the file, compare with gold_snips

    print('model: ', output)

    with open(current_folder + '/' + output) as f:
        lines = f.readlines()
        checklines = [l for l in lines if '### CT:' in l]
        quick_check = []
    for c in checklines:
        if '[[' in c:
            quick_check.append(1)
            # print('1 : ', c)
        else:
            quick_check.append(0)
            # print('0 :', c)
    short_check = quick_check[:2]
    short_check.extend(quick_check[3:])

    print(len(short_check), len(short_snips))
    # print(short_check)
    inds = [(i + 300,e) for i,e in enumerate(zip(short_snips, short_check)) if short_snips[i] != short_check[i]]
    print(inds)

    scores = precision_recall_fscore_support(short_snips, short_check, average='binary')
    print('Precision : {:.2f}, Recall : {:.2f}, F1 binary : {:.2f}'.format(scores[0], scores[1], scores[2]))
    print('-------------------------------------------')

#now handle llama_13 which is one shorter
print('model: ', llama_13b)

with open(current_folder + '/' + llama_13b) as f:
    lines = f.readlines()
    checklines = [l for l in lines if '### CT:' in l]
    quick_check = []
for c in checklines:
    if '[[' in c:
        quick_check.append(1)
    else:
        quick_check.append(0)

# print(short_check)

print(len(short_check), len(short_snips))
inds = [(i + 300,e) for i,e in enumerate(zip(short_snips, quick_check)) if short_snips[i] != quick_check[i]]
print(inds)

scores = precision_recall_fscore_support(short_snips, quick_check, average='binary')
print('Precision : {:.2f}, Recall : {:.2f}, F1 binary : {:.2f}'.format(scores[0], scores[1], scores[2]))
print('-------------------------------------------')


    # for game in games:
    #         ##STEP 1
    #     # if game['id'] in ['C120-B53-A4', 'C87-B25-A10', 'C49-B52-A27', 'C50-B15-A27', 'C157-B11-A7']:
    #         # text_list.append(game['id'])
    #         print(game['id'])
    #         game_id = game['id']
    #         text_list = []
    #         #make a list of edus w/ index
    #         #[[speaker, rels, text]]
    #         #then go through rels and plant them by index
    #         # [[speaker, [[0, Ack]], text]]
    #         #for list in edus list, add to text list :
    #         # 0. <Speaker> [0 Ack], text
    #         #see how this looks then figure out how to separate narrations
    #         edu_list = [[edu['speaker'], edu['text'],[]] for edu in game['edus']]
    #         for rel in game['relations']:
    #             if rel['type'] in ['Narration', 'Correction', 'Continuation', 'Result']: ##!! Just look at Corrections
    #                 edu_list[rel['y']][2].append([rel['x'], rel['type']])
    #         for i, item in enumerate(edu_list):
    #             item_string = str(i) + ' <' + item[0] + '> ' 
    #             ##check for NL moves
    #             if item[0] == 'Builder' and is_nl(item[1]):
    #                 item_string += decode(item[1])
    #             else:
    #                 item_string += item[1]
    #             ##add relations
    #             if len(item[2]) > 0:
    #                 item_string += '$$'
    #             for inc_rel in item[2]:
    #                 item_string += '[' + str(inc_rel[0]) + ',' + inc_rel[1] + '] '
    #             text_list.append(item_string)

    #         #now want to separate by Narrations. 
    #         narrations_dict = {} #json2
    #         narr_no = 0
    #         # narrations_list = []
    #         narrations_list = []
    #         for line in text_list:
    #             if ',Narration' in line and ',Result' in line:
    #                 narrations_dict[narr_no] = narrations_list
    #                 narr_no += 1
    #                 narrations_list = []
    #                 narrations_list.append(line)
    #             else:
    #                 narrations_list.append(line)
            
    #         # print(narrations_dict.keys())
    #         #STEP 2: remove anything that is not correction and remove snippets that do not contain moves
            
    #         hold = {'key': 'None', 'snip': 'None'}
    #         for key in sorted(narrations_dict.keys()):
    #             snip = narrations_dict[key]
    #             num_moves = 0
    #             corr = 0
    #             corr_triangle = 0
    #             for s in snip: 
    #                 if '|put' in s or '|remove' in s:
    #                     num_moves += 1
    #                 if ',Correction' in s:
    #                     corr += 1
    #                 if ',Correction' in s and ',Result' in s:
    #                     corr_triangle += 1
    #             if num_moves == 0 or (corr and not corr_triangle):
    #                 pass
    #             else:
    #                 #if correction, add it
    #                 #if not correction > 1 moves, add it
    #                 #if not correction == 1 moves, check next snippet 
    #                 if corr_triangle == 1 and num_moves == 2 and corr < 3:
    #                     snippet = {}
    #                     snippet['id'] = game_id + '_' + str(key)
    #                     snippet['corr'] = 1
    #                     snippet['text'] = snip
    #                     filtered_snippets.append(snippet)
    #                 else:
    #                     if num_moves > 1 and corr == 0:
    #                         snippet = {}
    #                         snippet['id'] = game_id + '_' + str(key)
    #                         snippet['corr'] = 0
    #                         snippet['text'] = snip
    #                         filtered_snippets.append(snippet)
    #                         #check for a previous unfiltered snippet
    #                         if hold['key'] != 'None' and key == hold['key'] + 1:
    #                             snippet = {}
    #                             snippet['id'] = game_id + '_' + str(hold['key'])
    #                             snippet['corr'] = 0
    #                             add_snip = []   
    #                             for s in snip:
    #                                 if '|put' in s or '|remove' in s:
    #                                     add_snip.append(s)
    #                                     break
    #                                 else:
    #                                     add_snip.append(s)
    #                             hold['snip'].extend(add_snip)
    #                             snippet['text'] = hold['snip']
    #                             snippet['ext'] = 1
    #                             filtered_snippets.append(snippet)
    #                             #put first move on snip and add
    #                             #clear hold dict
    #                             hold = {'key': 'None', 'snip': 'None'}
    #                     else:
    #                         #hold for next moves
    #                         pass
    #                         if num_moves == 1 and corr == 0:
    #                             #put in hold
    #                             hold['key'] = key
    #                             hold['snip'] = snip
    # """
    # NB:
    # For this first pass, we take only correction snippets that have 2 move turns and 
    # 2 corrections, and non-correction snippets that have 2 move turns, or one move turn 
    # then we add he first move turn of the next consecutive snippet if it is not a
    # correction
    # """
    # # ##to check the intermediate json
    # # print(len(filtered_snippets)) 
    # # print(len([i for i in filtered_snippets if i['corr'] == 1]))                     
    # # with open(current_folder+ '/akshay.json', 'w') as outfile:
    # #     json.dump(filtered_snippets, outfile)


    # #transform the json into a printable string
    # correction_count = 0 ##don't take more than 129 corrections
    # # number gotten from counts in json above
    # total_snippets = 0
    # for snip in filtered_snippets:
    #     if snip['corr'] == 1:
    #         if correction_count > 129:
    #             pass
    #         else:
    #             prompt_snippets.append(snip['id'] + '_CORRECTION')
    #             correction_count += 1
    #             total_snippets += 1
    #     else:
    #         prompt_snippets.append(snip['id'])
    #         total_snippets += 1
    #     for line in snip['text']:
    #         if '$$' in line and ',Correction' not in line:
    #             newline = line.split('$$')[0]
    #             prompt_snippets.append(newline)
    #         else:
    #             prompt_snippets.append(line)
    #     prompt_snippets.append('\n')

    # print(total_snippets, " total snippets")
    # print(correction_count - 1, " correction snippets")
    # print_string = '\n'.join(prompt_snippets)
    # with open (current_folder+ '/akshay.txt', 'w') as txt_file:
    #     txt_file.write(print_string)
    

