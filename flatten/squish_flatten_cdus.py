"""
Takes a json files of ANNOTATED games and returns a json with squished & flattened games
"""
import os 
import json 
import re
import datetime

current_folder=os.getcwd()

#open_path = current_folder + '/json/'
open_path = '/home/kate/minecraft_corpus/glozz_to_json/json_output/'

save_path = current_folder + '/json_squishflat/'

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

def text_replace(text):
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple', 'black']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    if 'puts' in text:
        replacement = 'puts down {} block. '.format(color[0])
    else:
        replacement = 'picks up {} block. '.format(color[0])
    return replacement

def squish_text(elements):
    text = []
    elements.sort(key = lambda x :x[1])
    squished = ''.join([s[3] for s in elements])
    return squished 

for f in json_files:
    if f == 'BRONZE_2023-03-17.json':
        with open(open_path + f, 'r') as jf:
            jfile = json.load(jf)
            for game in jfile:
                print(game['game_id'])
                replacements = {}
                squish = {}
                redundant = []
                #STEP 0: change all builder text in system moves
                for edu in game['edus']:
                    if edu['Speaker'] == 'System':
                        edu['text'] = text_replace(edu['text'])

                #STEP 1: pull elements from each CDU and find head edu
                #map cdu id to head element id

                edus = [(e['unit_id'], e['start_pos'], e['Speaker'], e['text']) for e in game['edus']]
                cdus = game['cdus']
                
                for cdu in cdus:
                    cid = cdu['schema_id']
                    print(cid)
                    elements = [elem for elem in edus if elem[0] in cdu['embedded_units']]
                    first = min(elements, key=lambda tup: tup[1])
                    head = first[0]
                    replacements[cid] = head
                    #STEP 2: check CDU components are all builder moves
                    if cdu_contents(elements):
                        #STEP 2.1: check if any of the elements has outgoing links (assume no incoming)
                        #if so, move x node of link to head?
                        outgoing_links = [r['x_id'] for r in game['relations']]
                        for e in elements:
                            if e[0] in outgoing_links:
                                replacements[e[0]] = head
                        #STEP 2.2: then move all text to head node and erase other edu elements
                        new_head_text = squish_text(elements)
                        squish[head] = new_head_text
                        for e in elements:
                            if e[0] != head:
                                redundant.append(e[0])
                        # redundant.extend([e[0] for e in elements if e[0] != head])

                #STEP 3: once you have your replacements, replace relation nodes
                for rel in game['relations']:
                    if rel['x_id'] in replacements:
                        rel['x_id'] = replacements[rel['x_id']]
                    if rel['y_id'] in replacements:
                        rel['y_id'] = replacements[rel['y_id']]
                #add squish text to head edu and remove other nodes
                new_edus = []
                for edu in game['edus']:
                    if edu['unit_id'] in squish.keys():
                        edu['text'] = squish[edu['unit_id']]
                        new_edus.append(edu)
                    elif edu['unit_id'] in redundant:
                        continue
                    else:
                        new_edus.append(edu)

                #replace edus field
                game['edus'] = new_edus
                #remove cdu field
                game['cdus'] = []
                #remove para field 
                game['paras'] = []
                #remove embedded cdus
                game['embedded_cdus'] = []

##re-save a new json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(save_path + now + '_squish_flat.json', 'w') as outfile:
    json.dump(jfile, outfile)

print('json saved')

            
            