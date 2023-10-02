"""
looks at performance on narration after second pass

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


def convert_rels(relist, rel_labels):
    """converts list of dicts to list of tuples, eg [(x,y,type)]"""
    newlist = []
    for r in relist:
        #newlist.append(tuple([int(r['x']), int(r['y']), rel_labels[r['type']]]))
        newlist.append(tuple([int(r['x']), int(r['y']), r['type']]))
    return newlist

current_dir = os.getcwd()
##try to open json file and check turns 
gold_annotations = 'TEST_30_bert.json'
bert_output = 'bert_multi_preds_30_katelinear.json'
narrations = 'narration_2p_pred_rels.json'

current_dir = os.getcwd()

gold = current_dir + '/jsons/' + gold_annotations
predicted = current_dir + '/jsons/' + bert_output
narrels = current_dir + '/jsons/' + narrations


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

try:
    with open(narrels, 'r') as f: 
        obj = f.read()
        narrs = json.loads(obj)
except IOError:
    print('cannot open json file ' + predicted)


all_golds = []
false_negs = []
true_pos = []
false_pos = []

narr_false_negs = []
narr_true_pos = []
narr_false_pos = []

max_len = 10
max_len_2p = 16

for game in gold_data:
    gold_id = game['id']
    gold_rels = game['relations']
    trans_gold_rels = convert_rels(gold_rels, rel_labels)

    # print(trans_gold_rels)

    bert_ids = [s['id'] for s in bert_data]

    # print('gold id {}'.format(gold_id))
    if gold_id in bert_ids:
        
        bert_rels = [g['pred_relations'] for g in bert_data if g['id'] == gold_id][0]

        narr_pass = [g['relations'] for g in narrs if g['id'] == gold_id][0]

        # print(bert_rels)
        trans_bert_rels = convert_rels(bert_rels, rel_labels)
        trans_narrs = convert_rels(narr_pass, rel_labels)

        #compare trans and bert rels

        tp = [r for r in trans_bert_rels if r in trans_gold_rels and r[2] == 'Narration']
        fp = [r for r in trans_bert_rels if r not in trans_gold_rels and r[2] == 'Narration']
        fn = [r for r in trans_gold_rels if r not in trans_bert_rels and r[2] == 'Narration']

        #comparison with added narrations
        ###!!! COUNT NUMBER OF DOUBLE-PREDICTED NARRS
        gold_narr = [r for r in trans_gold_rels if r[2] == 'Narration']
        narr_tp = [r for r in trans_narrs if r in gold_narr]
        narr_fp = [r for r in trans_narrs if r not in gold_narr]
        narr_fn = [r for r in gold_narr if r not in trans_narrs]

        # if len(trans_bert_rels) != (len(true_pos) + len(false_pos)):
        #     print('Not all rels accounted for in {} : {} != {} + {}'.format(gold_id, len(trans_bert_rels), (len(true_pos), len(false_pos))))
        #     print('Skipping game.')

        #add global dicts 
    
        for elem in tp:
            true_pos.append(elem[1] - elem[0])
        for elem in false_pos:
            false_pos.append(elem[1] - elem[0])
        for elem in fn:
            false_negs.append(elem[1] - elem[0])
        for elem in gold_narr:
            all_golds.append(elem[1] - elem[0])
        
        for elem in narr_tp:
            narr_true_pos.append(elem[1] - elem[0])
        for elem in narr_fp:
            narr_false_pos.append(elem[1] - elem[0])
        for elem in narr_fn:
            narr_false_negs.append(elem[1] - elem[0])


# change dicts into tables
# for each rel type, go to each dict and pull list of lengths
# fit lengths into a list of counts

sys.stdout = open('stats_predictions_narration.txt', 'w')

print('NARRATION RELATIONS')

all_gold = Counter([d for d in all_golds if d <= max_len])
true_pos = Counter([d for d in true_pos if d <= max_len])
false_pos = Counter([d for d in false_pos if d <= max_len])
false_neg = Counter([d for d in false_negs if d <= max_len])

lens = [l for l in range(1, max_len+1)]
data = []

    
for cnt in [all_gold, true_pos, false_pos, false_neg]:
    temp_lens = []
    for len in lens:
        temp_lens.append(cnt[len])
    data.append(temp_lens)

#now you have your lists of lists
#print tables

print('FIRST PASS')

left = ['Gold', 'True Pos', 'False Pos', 'False Neg']


print('                                         ')
head = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

prec, recall, f1 = get_scores(data)
print('Prec:' ,float(f'{prec:.2f}'), ' || Recall :',float(f'{recall:.2f}'), ' || F1 :', float(f'{f1:.2f}'))
print('                                         ')
print(pandas.DataFrame(data, left, head))
print('                                         ')
print('-----------------------------------------')
print('                                         ')




all_gold = Counter([d for d in all_golds if d <= max_len_2p])
true_pos = Counter([d for d in narr_true_pos if d <= max_len_2p])
false_pos = Counter([d for d in narr_false_pos if d <= max_len_2p])
false_neg = Counter([d for d in narr_false_negs if d <= max_len_2p])

lens = [l for l in range(1, max_len_2p+1)]
data = []

    
for cnt in [all_gold, true_pos, false_pos, false_neg]:
    temp_lens = []
    for len in lens:
        temp_lens.append(cnt[len])
    data.append(temp_lens)

#now you have your lists of lists
#print tables

print('SECOND PASS')

left = ['Gold', 'True Pos', 'False Pos', 'False Neg']


print('                                         ')
head = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

prec, recall, f1 = get_scores(data)
print('Prec:' ,float(f'{prec:.2f}'), ' || Recall :',float(f'{recall:.2f}'), ' || F1 :', float(f'{f1:.2f}'))
print('                                         ')
print(pandas.DataFrame(data, left, head))
print('                                         ')
print('-----------------------------------------')
print('                                         ')

sys.stdout.close()
