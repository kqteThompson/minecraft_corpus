"""
Takes output from second_pass.py and outputs a list of candidates, labels and raw text
for bert linear that considers only arch cans that have a non linguistic move between them. 

"""
import os 
import json 
import pickle
from collections import defaultdict, Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_out/'
save_path = current_folder + '/pickle_out/'

#running on training data:

# games = 'TRAIN_314_bert_2p2.json'
games = 'bert_multi_preds_30_2p2.json'
# games_save = 'TRAIN_314_bert_2p2.pck'
games_save = 'bert_multi_preds_30_2p2.pck'


#running on linear outputs:
# games = 'bert_multi_preds_30_second_pass.json'
# games_save = 'bert_multi_preds_2p1.pck'


final_candidates =  []

#for each game, get a list of turn no's after which there is a builder move
#then for edu in edu, if turn in list, then for every edu in that turn, make a candiate with every 
#other edu in all architect turns after.

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
   
    labels = []
    raw = []
    input_text = []

    for game_ind, game in enumerate(jfile):

        # print(game['id'])
        # make raw text 
        raw_text = [j["speaker"][:5] + ": " + j["text"] for j in game["edus"] ]

        raw += [raw_text]

        edus = game['edus']
        corrections = [(r['x'], r['y']) for r in game['relations']]
        # print('corrections :', corrections)

        #get consective NL-NL pairs
        pairs = []

        nls = [edu for edu in edus if edu['type'] == 0]
        for pair in [nls[i:i+2] for i in range(len(nls)-1)]:
            pairs.append(pair)

        for pair in pairs:
            
            start = pair[0]['global_index']
            end = pair[1]['global_index']
            # print('start, end: ', start, end)
            cand = [game_ind, start, end, 0, -1, 0]
            if (start, end) in corrections:
                cand[3] = 1
                cand[4] = 2

            #get number of architect turns between them
            slice = edus[start:end]
            inter_arch = []
            for sl in slice:
                if sl['speaker'] == 'Architect':
                    inter_arch.append(sl['global_index'])
            
            if len(inter_arch) > 0:
                # print(inter_arch)
                for i in inter_arch:
                    if (start, i) in corrections:
                        cand[5] = 1

            #print(cand)              
            labels.append(cand)
            input_text.append([raw_text[cand[1]], raw_text[cand[2]]])

    #check outputs
    # print(len(labels))
    # print('both:')
    # print(len([l for l in labels if l[3] == 1 and l[5] == 1]))
    # print('just NL-NL')
    # print(len([l for l in labels if l[3] == 1 and l[5] == 0]))
    # print('just NL-A')
    # print(len([l for l in labels if l[3] == 0 and l[5] == 1]))

         
    # # use this to see the distance distributions
    # # distances = [abs(i[2] - i[1]) for i in labels if i[3] == 1]
    # # dist_cnts = Counter(distances)
    # # cntslist = list(dist_cnts.items())
    # # cntslist.sort(key=lambda x:x[0])

    # # for c in cntslist:
    # #     print(c[0], [c[1]])
 

final_outputs = [raw, input_text, labels]
#Now pickle these three to fee to linear model
pickle_path = save_path + games_save

with open(pickle_path, 'wb') as f:
    pickle.dump(final_outputs, f)


