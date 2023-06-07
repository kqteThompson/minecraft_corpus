"""
Takes a json files of ANNOTATED games and returns a json with squished & flattened games
Grosso modo:
NEW in V2: special handling of linguistics CDUS:
    a. all narrations in coming and outgoing to head
    b. all other incoming links to head and all other outgoing links out of tail. 
    c. all non-element 'danglers' that are "inside" the boundaries of the CDUs are ???
1. For each EDU, if speaker == 'System', replace the text with simplified move text
2. For each CDU, if it is a builder moves CDU: 
    2.1. Find the last EDU, creating a *replacements* dict that maps CDU ids to last id
    2.2. For each EDU, if there is an outgoing link, add EDU id : last id to *replacements*
    AND add dangler ids to *targets* dict to change start position of edu (so they go below the action block)
    AND add all outgoing links from the CDU itself to the *cdu_outgoing* dict, so that
    if the target EDU is "within" the CDU, it will be moved below.
    2.3. For each EDU that is not the last, gather the text and squish into one block
    and assign to the last edu by adding to the dict *squish*, mapping last id : squish text
    2.4. Add all non-last EDU ids to the *redundant* list to be removed 
3. For each CDU, if it is not a builder moves CDU:
    3.1 Find the head EDU
    3.2 For every head EDU, add CDU id : head id
4. Go through and do all replacements

NB: the output of this script is only useful as an input to a BERT formatting script.
If you want to visualize with GLOZZ, BERT format first then use BERT to GLOZZ formatting.
"""
import os 
import json 
import re
import datetime
from collections import defaultdict

current_folder=os.getcwd()

#open_path = current_folder + '/json/'
# open_path = '/home/kate/minecraft_corpus/glozz_to_json/json_output_frozen/'
open_path = '/home/kate/minecraft_corpus/glozz_to_json/json_output_test_batch/'

save_path = current_folder + '/json_squishflat_test_batch/'

json_files = os.listdir(open_path)

def cdu_contents(edus):
    """
    takes CDU elements and returns 1 if CDU is all builder moves
    """
    contents = 0
    speakers = list(set([e[2] for e in edus]))
    if len(speakers) == 1 and speakers[0] == 'System':
        contents = 1

    return contents

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            print(game['game_id'])
            replacements = {}
            ling_replacements_x = {} # relation_id : new x id
            ling_replacements_y = {} # relation_id : new y id
            redundant = []
           
            #STEP 1: pull elements from each CDU 
            edus = [(e['unit_id'], e['start_pos'], e['Speaker'], e['text']) for e in game['edus']]
            cdus = game['cdus']

            #STEP 1.2: create links dicts (only need to do this once)
            outgoing_links = defaultdict(list)
 
            for rel in game['relations']:
                outgoing_links[rel['x_id']].append((rel['y_id'], rel['type'], rel['relation_id']))

            incoming_links = defaultdict(list)
            for rel in game['relations']:
                incoming_links[rel['y_id']].append((rel['x_id'], rel['type'], rel['relation_id']))

            
            for cdu in cdus:
                cid = cdu['schema_id']
                elements = [elem for elem in edus if elem[0] in cdu['embedded_units']]
                
             
                #STEP 2: if not components builder moves:
                if not cdu_contents(elements):
                    redundant.append(cid)

                    first = min(elements, key=lambda tup: tup[1])
                    head = first[0]
                    last = max(elements, key=lambda tup: tup[1])
                    tail = last[0]

                    #STEP 3.1: change relevant endpoints of relations connecing to linguistic CDUS
                   
                    #for link in outgoing links, if the source is the CDU, make the source the CDU tail unless 
                    #the relation type is 'narration', then head
                    for target in outgoing_links:
                        if cid in outgoing_links.keys():
                            for link in outgoing_links[cid]:
                                if link[1] == 'Narration':
                                    #then put on head
                                    ling_replacements_x[link[2]] = head
                                else:
                                    #put on tail
                                    ling_replacements_x[link[2]] = tail

                    #for link in incoming links, if the target is the CDU, make the target the head
                    for source in incoming_links:
                        if cid in incoming_links.keys():
                            for link in incoming_links[cid]:
                                ling_replacements_y[link[2]] = head

            #STEP 4: once we have all replacements, replace ids in relation nodes
            for rel in game['relations']:
                if rel['relation_id'] in ling_replacements_x.keys():
                    rel['x_id'] = ling_replacements_x[rel['relation_id']]
                if rel['relation_id'] in ling_replacements_y.keys():
                    rel['y_id'] = ling_replacements_y[rel['relation_id']]

            #add squish text to tail edu and remove other nodes
            #NB: we remove by creating a new edu array
            new_cdus = []
            for cdu in game['cdus']:
                if cdu['schema_id'] in redundant:
                    continue
                else:
                    new_cdus.append(cdu)

            #remove flattened CDUs but keep builder move CDUs            
            game['cdus'] = new_cdus
            #keep para field 
            #remove embedded cdus
            game['embedded_cdus'] = []

##re-save a new json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(save_path + now + '_flat.json', 'w') as outfile:
    json.dump(jfile, outfile)

print('json saved')

            
            