"""
Create data for comparison tables
Takes a gold json and bert output json and returns a comparison by type and relation distance

"""
import os
import json
from collections import defaultdict, Counter
import pandas 

rel_labels = {'Comment': 0, 'Contrast': 1, 'Correction': 2, 'Question-answer_pair': 3, 'Parallel': 4, 'Acknowledgement': 5,
            'Elaboration': 6, 'Clarification_question': 7, 'Conditional': 8, 'Continuation': 9, 'Result': 10, 'Explanation': 11,
            'Q-Elab': 12, 'Alternation': 13, 'Narration': 14, 'Confirmation_question': 15, 'Sequence' : 17, 'Background': 18}

reverse_map = {0: 'Comment', 1:'Contrast', 2:'Correction', 3:'QAP', 4:'Parallel', 5:'Acknowledgement',
            6:'Elaboration', 7:'Clarification_question', 8:'Conditional', 9:'Continuation', 10:'Result', 11:'Explanation',
            12:'Q-Elab', 13:'Alternation', 14:'Narration', 15:'Conf-Q', 17:'Sequence', 18:'Background'}

def convert_rels(relist, rel_labels):
    """converts list of dicts to list of tuples
    ex: [(1,2,5), (1,3,4)]
    """
    newlist = []
    for r in relist:
        newlist.append(tuple([int(r['x']), int(r['y']), rel_labels[r['type']]]))
    return newlist

def find_multi_parents(relist):
    """takes a list of relations and returns a list of lists of multi relation types
    ex: [[3,3,2], [1,2], [3,3]]
    """
    cnt = defaultdict(list)
    for rel in relist:
        cnt[rel[1]].append(rel[2])
    multi_types = [c[1] for c in cnt.items() if len(c[1]) > 1]
    return multi_types

current_dir = os.getcwd()

##try to open json file and check turns 
# gold_annotations = 'TEST_67_bert.json'
# bert_output = 'bert_multi_preds_67.json'
gold_annotations = 'TEST_30_bert.json'
bert_output = 'bert_multi_preds_30.json'

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

#add multi parent information here
#simply add the relation types
# true_pos_multi_cnt = []
# false_pos_multi_cnt = []

max_len = 10

total_gold_mults = []
true_pos_mults = []

for game in gold_data:
    gold_id = game['id']
    gold_rels = game['relations']
    trans_gold_rels = convert_rels(gold_rels, rel_labels)
    #process gold rels
    
    
    bert_ids = [s['id'] for s in bert_data]

    if gold_id in bert_ids:
        bert_rels = [g['pred_relations'] for g in bert_data if g['id'] == gold_id][0]
        trans_bert_rels = convert_rels(bert_rels, rel_labels)

        #find number of multi parents in gold then see overlap with bert preds
        #find the elements of trans_gold_rels where the y coord is repeated
        cnt = defaultdict(list)
        for rel in trans_gold_rels:
            cnt[rel[1]].append(rel)
        gold_mults = []
        for rel in [c[1] for c in cnt.items() if len(c[1])>1]:
            gold_mults.extend(rel)
            #now gold mult should be a subset of trans_gold_rels
            total_gold_mults.extend(gold_mults)

        for rel in trans_bert_rels:
            if rel in gold_mults:
                true_pos_mults.append(rel)
                #now true_pos_mults should be a subset of trans_bert_mults

# print(total_gold_mults)
# print(true_pos_mults)
#now you have two lists of all the multi-parent relations in both gold and bert
mlt_gold = find_multi_parents(total_gold_mults)
mlt_pred = find_multi_parents(true_pos_mults)
# #wait...need to make sure these SAME relations are in bert preds

print(mlt_gold)
          
# #make true and false positive multi parent counts
# #so now should have totals list that is all the relation types for multi parent edus
# tru_multi_counts = defaultdict(list)
# all_lengths = []
# for t in mlt_gold:
#     l = len(t)
#     all_lengths.append(len(t)) #to figure out the range of lens
#     for i in t:
#         tru_multi_counts[i].append(l)

# head = list(set(all_lengths))
# head.sort()
# labels = []
# data = []
# for k in tru_multi_counts.keys():
#     labels.append(reverse_map[k])
#     counts = Counter(tru_multi_counts[k])
#     data.append([counts[n] for n in head])
# print('Gold multi-parent relations')
# print('                                         ')
# print(pandas.DataFrame(data, labels, head))
# print('                                         ')   


# tru_multi_counts = defaultdict(list)
# all_lengths = []
# for t in mlt_pred:
#     l = len(t)
#     all_lengths.append(len(t)) #to figure out the range of lens
#     for i in t:
#         tru_multi_counts[i].append(l)

# head = list(set(all_lengths))
# head.sort()
# labels = []
# data = []
# for k in tru_multi_counts.keys():
#     labels.append(reverse_map[k])
#     counts = Counter(tru_multi_counts[k])
#     data.append([counts[n] for n in head])
# print('Predicted multi-parent relations')
# print('                                         ')
# print(pandas.DataFrame(data, labels, head))
# print('                                         ')   





