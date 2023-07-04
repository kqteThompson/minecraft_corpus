"""
Takes a json of games and sample ids to remove from the BAP data 
returns an amended data set to run anyway
snippets = {game_id : [list of sample ids to keep]}

len of train data 4453
1082 samples skipped
161 games replaces with our snippets

"""
import os
import json
import pickle
from utils import BuilderAction


current_folder=os.getcwd()

#open json
json_open = current_folder + '/snippets_2023-06-29.json'
#open train_data
data_open = current_folder + '/generated_data/train-jsons.pkl'

save_file = current_folder + '/generated_data/new-train-jsons.pkl'

with open(data_open, 'rb') as handle:
    bap_data = pickle.load(handle)

with open(json_open, 'r') as jf:
    snippets = json.load(jf)

new_bap = []
samples_skipped = 0
for sample in bap_data:
    if sample['orig_experiment_id'] in snippets.keys():
        if sample['sample_id'] in snippets[sample['orig_experiment_id']]:
            new_bap.append(sample)
        else:
            samples_skipped += 1
    else:
        new_bap.append(sample)
    
print('{} samples skipped'.format(samples_skipped))
print('{} games replaces with our snippets'.format(len(snippets)))

#save new data
with open(save_file, 'wb') as f:
    pickle.dump(new_bap, f, protocol=3)