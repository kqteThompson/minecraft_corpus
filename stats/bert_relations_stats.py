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

# def find_multi_parents(relist):
#     """takes a list of relations and returns a list of lists of multi relation types"""
#     cnt = defaultdict(list)
#     for rel in relist:
#         cnt[rel[1]].append(rel[2])
#     multi_types = [c[1] for c in cnt.items() if len(c[1]) > 1]
#     return multi_types

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
# gold_annotations = 'TEST_30_bert.json'
# bert_output = 'bert_multi_preds_30.json'
gold_annotations = 'TEST_30_minus_narr-corr.json'
bert_output = 'bert_multi_preds_30_nocn.json'

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

gold_dict = defaultdict(list)
true_pos_dict = defaultdict(list)
false_pos_dict = defaultdict(list)

#add multi parent information here
#simply add the relation types
true_pos_multi_cnt = []
false_pos_multi_cnt = []

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
        #add to multiparent counts
        # mppos = find_multi_parents(true_pos)
        # if len(mppos) > 0:
        #     true_pos_multi_cnt.extend(mppos)
        # mpfls = find_multi_parents(false_pos)
        # if len(mpfls) > 0:
        #     false_pos_multi_cnt.extend(mpfls)
        
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
#so sometimes there is no data for a certain relation type in the predicted data

final_dict = defaultdict(list)
for key in list(gold_dict.keys()):
    lens = Counter([d for d in gold_dict[key] if d <= max_len])
    final_lens = []
    for dist in range(1,max_len+1):
        num = lens[dist]
        final_lens.append(num)
    final_dict[key].append(final_lens)
    for dictionary in [true_pos_dict, false_pos_dict]:
        final_predlens = []
        if key in dictionary.keys():
            predlens = Counter([d for d in dictionary[key] if d <= max_len])
            for dist in range(1, max_len+1):
                nums = predlens[dist]
                final_predlens.append(nums)
        else:
            print('NO {} relation in dict'.format(key))
            nums = [0 for i in range(1, max_len+1)]
            final_predlens = nums

        final_dict[key].append(final_predlens)

#check that all have three lists
for rel_type in list(final_dict.keys()):
    if len(final_dict[rel_type]) < 3:
        print('{} only has {} row'.format(rel_type, len(final_dict[rel_type])))

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


#make true and false positive multi parent counts
#so now should have totals list that is all the relation types for multi parent edus
# tru_multi_counts = defaultdict(list)
# all_lengths = []
# for t in true_pos_multi_cnt:
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
# print('True positive relations in multi-parent edus')
# print('                                         ')
# print(pandas.DataFrame(data, labels, head))
# print('                                         ')   


# false_multi_counts = defaultdict(list)
# all_lengths = []
# for t in false_pos_multi_cnt:
#     l = len(t)
#     all_lengths.append(len(t)) #to figure out the range of lens
#     for i in t:
#         false_multi_counts[i].append(l)

# head = list(set(all_lengths))
# head.sort()
# labels = []
# data = []
# for k in false_multi_counts.keys():
#     labels.append(reverse_map[k])
#     counts = Counter(false_multi_counts[k])
#     data.append([counts[n] for n in head])

# print('False positive relations in multi-parent edus')
# print('                                         ')
# print(pandas.DataFrame(data, labels, head))
# print('                                         ')  



