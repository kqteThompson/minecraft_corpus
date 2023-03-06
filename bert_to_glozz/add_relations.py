'''
input: json output with relations from bert csv, and the squished data json that was
originally fed to bert
NB: also changes builder non-linguistic moves back to 'System' speaker
output: a squished data json with predicted relations (to be fed to glozz file generator)
'''
import os
import json


def check_text(text):
    check = 0 
    if 'puts down a' in text:
        check = 1
    if 'picks up a' in text:
        check = 1
    return check

predicted_relations = 'predictions-2.json'
data = '/home/kate/minecraft_corpus/bert/json_squished_out/2023-03-01BRONZE_dev_10_bert_squished.json'

save = 'bert_pred.json'

current_folder=os.getcwd()

rel_path = current_folder + '/' + predicted_relations
data_path = data

output_path= current_folder + '/' + save

with open(rel_path, 'r') as jf:
    rels = json.load(jf)

with open(data_path, 'r') as jf:
    edus = json.load(jf)

new_rels = {}
for rel in rels:
    new_rels[rel['id']] = rel['relations']

for edu in edus:
    game_id = edu['id']
    print(game_id)
    edu['relations'] = new_rels[game_id]   

    #change builder back to system where needed
    for elem in edu['edus']:
        if elem['speaker'] == 'Builder':
            check = check_text(elem['text'])
            if check:
                elem['speaker'] = 'System'

#save json
with open(output_path, "w") as outfile:
    json.dump(edus, outfile)
