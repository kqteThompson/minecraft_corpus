#open CSV
#for every line in csv, if in val set
#then for every line of that id, create an {}
#id: ___, edus: [{}], relations:[{}]

import os
import csv
import json

map_relations = {'Comment': 0, 'Contrast': 1, 'Correction': 2, 'Question-answer_pair': 3, 
'QAP': 3, 'Parallel': 4, 'Acknowledgement': 5,'Elaboration': 6, 'Clarification_question': 7, 
'Conditional': 8, 'Continuation': 9, 'Result': 10, 'Explanation': 11,'Q-Elab': 12, 
'Alternation': 13, 'Narration': 14, 'Background': 15, 'Break': 16, 'Sequence' : 17}

current_folder = os.getcwd()
mincraft_csv = current_folder + '/predictions-2.csv'


new_relation_dict = {v: k for k, v in map_relations.items()}
dialogues = []
last_id = 0

with open(mincraft_csv, 'r') as read_obj:
    output = csv.reader(read_obj)
    csv = list(output)
    relations = []
    last_id = csv[1][1]
    print("starting last id is {}".format(last_id))
    for row in csv[1:]:
        game_id = row[1]
        if game_id != last_id:
            print(game_id)
            if len(relations) > 1: #if there were already relations then put them away
                d = {}
                d['id'] = last_id
                d['relations'] = relations
                dialogues.append(d)
                relations = []
            last_id = game_id
            relation = {}
            relation['type'] = new_relation_dict[int(row[7])]
            relation['x'] = row[3]
            relation['y'] = row[4]
            relations.append(relation)
        else:
            relation = {}
            relation['type'] = new_relation_dict[int(row[7])]
            relation['x'] = row[3]
            relation['y'] = row[4]
            relations.append(relation)
    if len(relations) > 1:
        d = {}
        d['id'] = game_id
        d['relations'] = relations
        dialogues.append(d)

##save json

with open(current_folder + "/predictions-2.json", "w") as outfile:
    json.dump(dialogues, outfile)


