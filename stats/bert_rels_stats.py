"""
Create data for comparison tables
Takes a gold json and bert output json and returns a comparison by type and relation distance

"""
import os
import json
import sys
from collections import defaultdict, Counter
import pandas 


"""
make four big dicts for 4 types, with keys that are rel types
For each game, 
get a list of all gold, all false neg (gold that's not in pred), false pos (pred that's not in gold) and true pos.
[(x,y,type)]

"""

rel_labels = {'Comment': 0, 'Contrast': 1, 'Correction': 2, 'Question-answer_pair': 3, 'Parallel': 4, 'Acknowledgement': 5,
            'Elaboration': 6, 'Clarification_question': 7, 'Conditional': 8, 'Continuation': 9, 'Result': 10, 'Explanation': 11,
            'Q-Elab': 12, 'Alternation': 13, 'Narration': 14, 'Confirmation_question': 15, 'Sequence' : 17, 'Background': 18}

reverse_map = {0: 'Comment', 1:'Contrast', 2:'Correction', 3:'QAP', 4:'Parallel', 5:'Acknowledgement',
            6:'Elaboration', 7:'Clarification_question', 8:'Conditional', 9:'Continuation', 10:'Result', 11:'Explanation',
            12:'Q-Elab', 13:'Alternation', 14:'Narration', 15:'Conf-Q', 17:'Sequence', 18:'Background'}


def convert_rels(relist, rel_labels):
    """converts list of dicts to list of tuples, eg [(x,y,type)]"""
    newlist = []
    for r in relist:
        newlist.append(tuple([int(r['x']), int(r['y']), rel_labels[r['type']]]))
    return newlist


##try to open json file and check turns 
gold_annotations = 'TEST_30_bert.json'
bert_output = 'bert_multi_preds_30_katelinear.json'

current_dir = os.getcwd()

gold = current_dir + '/jsons/' + gold_annotations
predicted = current_dir + '/jsons/' + bert_output

try:
    with open(gold, 'r') as f: 
        obj = f.read()
        gold_data = json.loads(obj)
except IOError:
    print('cannot open json file ' + gold)

try:
    with open(predicted, 'r') as f: 
        obj = f.read()
        bert_data = json.loads(obj)
except IOError:
    print('cannot open json file ' + predicted)


all_gold = defaultdict(list)
false_neg = defaultdict(list)
false_pos = defaultdict(list)
true_pos = defaultdict(list)


for game in gold_data:
    gold_id = game['id']
    gold_rels = game['relations']
    trans_gold_rels = convert_rels(gold_rels, rel_labels)

def get_scores(datalist):
    """returns precision, recall and f1 for one relation type"""
    tp = sum(datalist[1])
    fp = sum(datalist[2])
    fn = sum(datalist[3])
    if tp == 0:
        p = 0
        r = 0
        f1 = 0
    else:
        p = tp*1.0/(tp + fp)*1.0
        r = tp*1.0/(tp + fn)*1.0
        f1 = 2*(p*r/(p+r))
    return p, r, f1

current_dir = os.getcwd()

##try to open json file and check turns 
gold_annotations = 'TEST_30_bert.json'
bert_output = 'bert_multi_preds_30_katelinear.json'
# gold_annotations = 'TEST_30_minus_narr-corr.json'
# bert_output = 'bert_multi_preds_30_nocn.json'

all_gold_dict = defaultdict(list)  #keys are rel types, values are lengths
false_neg_dict = defaultdict(list)
true_pos_dict = defaultdict(list)
false_pos_dict = defaultdict(list)


max_len = 10

for game in gold_data:
    gold_id = game['id']
    gold_rels = game['relations']
    trans_gold_rels = convert_rels(gold_rels, rel_labels)

    # print(trans_gold_rels)

    bert_ids = [s['id'] for s in bert_data]

    # print('gold id {}'.format(gold_id))
    if gold_id in bert_ids:
        
        bert_rels = [g['pred_relations'] for g in bert_data if g['id'] == gold_id][0]

        # print(bert_rels)
        trans_bert_rels = convert_rels(bert_rels, rel_labels)

        # # figure out just the scores for relation types:
        # #WIP -- so we can see the type scores...
        # gold_attach = {(a[0], a[1]):a[2] for a in trans_gold_rels}
        # bert_attach = {(a[0], a[1]):a[2] for a in trans_bert_rels}


        #compare trans and bert rels

        true_pos = [r for r in trans_bert_rels if r in trans_gold_rels]
        false_pos = [r for r in trans_bert_rels if r not in trans_gold_rels]
        false_neg = [r for r in trans_gold_rels if r not in trans_bert_rels]

        if len(trans_bert_rels) != (len(true_pos) + len(false_pos)):
            print('Not all rels accounted for in {} : {} != {} + {}'.format(gold_id, len(trans_bert_rels), (len(true_pos), len(false_pos))))
            print('Skipping game.')

        #add global dicts 

        for elem in true_pos:
            true_pos_dict[elem[2]].append(elem[1] - elem[0])
        for elem in false_pos:
            false_pos_dict[elem[2]].append(elem[1] - elem[0])
        for elem in false_neg:
            false_neg_dict[elem[2]].append(elem[1] - elem[0])
        for elem in trans_gold_rels:
            all_gold_dict[elem[2]].append(elem[1] - elem[0])

#change dicts into tables
# for each rel type, go to each dict and pull list of lengths
# fit lengths into a list of counts

# sys.stdout = open('stats_predictions_relations.txt', 'w')

# for k in all_gold_dict.keys():

#     all_gold = Counter([d for d in all_gold_dict[k] if d <= max_len])
#     true_pos = Counter([d for d in true_pos_dict[k] if d <= max_len])
#     false_pos = Counter([d for d in false_pos_dict[k] if d <= max_len])
#     false_neg = Counter([d for d in false_neg_dict[k] if d <= max_len])

#     lens = [l for l in range(1, max_len+1)]
#     data = []

    
#     for cnt in [all_gold, true_pos, false_pos, false_neg]:
#         temp_lens = []
#         for len in lens:
#             temp_lens.append(cnt[len])
#         data.append(temp_lens)

#     #now you have your lists of lists
#     #print tables

#     print('{} RELATIONS'.format(reverse_map[k]))
 
#     left = ['Gold', 'True Pos', 'False Pos', 'False Neg']

    
#     print('                                         ')
#     head = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#     prec, recall, f1 = get_scores(data)
#     print('Prec:' ,float(f'{prec:.2f}'), ' || Recall :',float(f'{recall:.2f}'), ' || F1 :', float(f'{f1:.2f}'))
#     print('                                         ')
#     print(pandas.DataFrame(data, left, head))
#     print('                                         ')
#     print('-----------------------------------------')
#     print('                                         ')

# sys.stdout.close()
