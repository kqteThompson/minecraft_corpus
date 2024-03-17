import os
import json
from sklearn.metrics import precision_recall_fscore_support

"""
print out json created from fuse docs
"""

current_folder=os.getcwd()

fuse = 'short_snips.json'

with open(current_folder + '/' + fuse) as f:
    jfile = json.load(f)
    output = jfile

#chose the model you want to see
# model = 'llama_7b'
model = 'llama_13b'
# model = 'mistral'

fuse_list = []

exact_match_count = 0
non_exact_match_count = 0
no_corr_count = 0
total_snippets = len(output)
for o in output:
    text = o['sample'].split('\n')
    for t in text:
       fuse_list.append(t)
    fuse_list.append('\n')
    gc = o['corrections']['gold'].strip()
    fuse_list.append('GOLD : ' + gc)
    k = [key for key in o['corrections'].keys() if model in key]
    mc = o['corrections'][k[0]].strip()
    fuse_list.append(model + ': ' + mc)
    ###check if gc and mc output is the same
    if gc != '[]':
        if gc == mc:
            fuse_list.append('EXACT CORRECTION MATCH')
            exact_match_count += 1
        else:
            if mc == '[]':
                fuse_list.append('false negative')
                no_corr_count += 1
            else:
                fuse_list.append('NO EXACT MATCH')
                non_exact_match_count += 1
    else:
        no_corr_count += 1
        if gc != mc:
            fuse_list.append('false positive')
            no_corr_count += 1
        else:
            fuse_list.append('true negative')
    fuse_list.append('\n')
total_counts = ('exact correction matches : {}, non-exact correction matches : {}, false pos/neg : {}, total exmaples : {} \n'.format(exact_match_count, non_exact_match_count, no_corr_count, total_snippets))
final_fuse = [total_counts] + fuse_list

print_string = '\n'.join(final_fuse)
with open (current_folder+ '/results_' + model + '.txt', 'w') as txt_file:
    txt_file.write(print_string)
    

