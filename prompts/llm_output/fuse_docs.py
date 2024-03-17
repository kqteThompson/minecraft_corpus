import os
import json
from sklearn.metrics import precision_recall_fscore_support

"""
put all model answers and gold under each snippet
use llama_13b since it's shorter
"""

current_folder=os.getcwd()


llama_7b = 'llama_7b_mc_output.txt'
llama_13b = 'llama_13b_mc_output.txt'
mistral = 'mistral_7b_mc_output.txt'

gold_corp = 'minecraft-corrections.jsonl'


gold = []
with open(current_folder + '/' + gold_corp) as f:
    for line in f:
        gold.append(json.loads(line))

#change format of gold_snips
gold_snips = []
for g in gold[300:]:
    new = {}
    new['sample'] = g['sample']
    new['corrections'] = {}
    new['corrections']['gold'] = str(g['CT'])
    gold_snips.append(new)

#remove 3 because not present in llama_13b
short_snips = gold_snips[:2]
short_snips.extend(gold_snips[3:])
# print(short_snips)

checks = [] #put all outputs here
for output in [llama_7b, mistral]:
    #open the file, compare with gold_snips

    print('model: ', output)

    with open(current_folder + '/' + output) as f:
        lines = f.readlines()
        checklines = [l for l in lines if '### CT:' in l]
        
    short_check = checklines[:2]
    short_check.extend(checklines[3:])

    for i,c in enumerate(short_check):
        a = c.split(':')[1]
        if 'None' in a:
            short_snips[i]['corrections'][output] = '[]'
        else:
            short_snips[i]['corrections'][output] = a

#now handle llama_13 which is one shorter
print('model: ', llama_13b)

with open(current_folder + '/' + llama_13b) as f:
    lines = f.readlines()
    checklines = [l for l in lines if '### CT:' in l]
for i,c in enumerate(checklines):
    a = c.split(':')[1]
    if 'None' in a:
        short_snips[i]['corrections'][llama_13b] = '[]'
    else:
        short_snips[i]['corrections'][llama_13b] = a



print(len(short_snips))                   
with open(current_folder+ '/short_snips.json', 'w') as outfile:
    json.dump(short_snips, outfile)


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
    

