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
    """converts list of dicts to list of tuples"""
    newlist = []
    for r in relist:
        newlist.append(tuple([int(r['x']), int(r['y']), rel_labels[r['type']]]))
    return newlist

def get_scores(datalist):
    """returns precision, recall and f1 for one relation type"""
    tp = sum(datalist[1])
    fp = sum(datalist[2])
    gold = sum(datalist[0])
    fn = gold - tp
    if tp == 0 or fp == 0 :
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
# gold_annotations = 'TEST_67_bert.json'
# bert_output = 'bert_multi_preds_67.json'
gold_annotations = 'TEST_30_bert.json'
bert_output = 'bert_multi_preds_30.json'

gold = current_dir + '/' + gold_annotations
predicted = current_dir + '/' + bert_output

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

gold_dict = defaultdict(list)
true_pos_dict = defaultdict(list)
false_pos_dict = defaultdict(list)

max_len = 10

for game in gold_data:
    gold_id = game['id']
    gold_rels = game['relations']
    trans_gold_rels = convert_rels(gold_rels, rel_labels)
    #process gold rels
    
    
    bert_ids = [s['id'] for s in bert_data]

    if gold_id in bert_ids:
        bert_rels = [g['pred_relations'] for g in bert_data if g['id'] == gold_id][0]
        trans_bert_rels = convert_rels(bert_rels, rel_labels)
        true_pos = []
        false_pos = []
        for rel in trans_bert_rels:
            if rel in trans_gold_rels:
                true_pos.append(rel)
            else:
                false_pos.append(rel)
        if len(trans_bert_rels) != (len(true_pos) + len(false_pos)):
            print('Not all rels accounted for in {} : {} != {} + {}'.format(gold_id, len(trans_bert_rels), (len(true_pos), len(false_pos))))
            print('Skipping game.')
        else:
            for j in true_pos:
                true_pos_dict[reverse_map[j[2]]].append(abs(j[0]-j[1]))
            for k in false_pos:
                false_pos_dict[reverse_map[k[2]]].append(abs(k[0]-k[1]))
    else:
        print('Could not locate {} in bert ids'.format(gold_id))

    for i in trans_gold_rels:
        gold_dict[reverse_map[i[2]]].append(abs(i[0]-i[1]))

print('Done with first counts')

final_dict = defaultdict(list)
for dictionary in [gold_dict, true_pos_dict, false_pos_dict]:
    for key in list(dictionary.keys()):
        lens = Counter([d for d in dictionary[key] if d <= max_len])
        final_lens = []
        for dist in range(1,11):
            num = lens[dist]
            final_lens.append(num)
        final_dict[key].append(final_lens)

print(list(final_dict.keys()))
print(final_dict['Conditional'])

#check that all have three lists
for rel_type in list(final_dict.keys()):
    if len(final_dict[rel_type]) < 3:
        print('{} only has {} row'.format(rel_type, len(final_dict[rel_type])))

final_dict['Conditional'].extend([[0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]])
final_dict['Explanation'].extend([[0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0]])
final_dict['Sequence'] = [final_dict['Sequence'][0], [0,0,0,0,0,0,0,0,0,0], final_dict['Sequence'][1]]

print(final_dict['Explanation'])
print(final_dict['Conditional'])
print(final_dict['Sequence'])

#print tables

for rel_type in list(final_dict.keys()):

    data = final_dict[rel_type]
    left = ['Gold', 'True Pos', 'False Pos']
    print('                                         ')
    head = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    print(rel_type)
    prec, recall, f1 = get_scores(data)
    print('Prec:' ,float(f'{prec:.2f}'), ' || Recall :',float(f'{recall:.2f}'), ' || F1 :', float(f'{f1:.2f}'))
    print('                                         ')
    print(pandas.DataFrame(data, left, head))
    print('                                         ')
    print('-----------------------------------------')
    print('                                         ')






