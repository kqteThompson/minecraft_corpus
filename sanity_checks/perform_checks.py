import os
import json
# from collections import Counter, defaultdict
"""
perform basic checks on annotations
input a json containing game(s)
output a txt file in logs for each game that has issues
"""

#empty CDUs
#CDUs containing CDUS 
#CDU punctures -- make sure that relations from edus of one cdu to relations of another cdu
#contained by first CDU aren't considered punctures  !!WIP
#every edu and cdu has at least one incoming link (or is a part of a CDU) !!WIP


current_folder=os.getcwd()

# games_path = current_folder + '../glozz_to_json/bronze_json_output/'
games_path = '/home/kate/minecraft_corpus/glozz_to_json/json_output/'

log_path = current_folder + '/check_logs/'
if not os.path.isdir(log_path):
    os.makedirs(log_path)

games_pass = []

folder_array = os.listdir(games_path) 

# for f in folder_array:
for f in [s for s in folder_array if s == 'SILVER_2023-11-13.json']:
    print("Checking  " + f)
    print('------------')
    with open(games_path + f, 'r') as j:
        jfile = json.load(j)
        games = jfile
    
    print("Number of games: {}".format(len(games)))

    counter = 1
    for game in games:
        game_name = game['game_id']
        print("Looking at game number {},  {}".format(counter, game_name))
        counter += 1
        log_string = ""
        print("{} EDUs".format(len(game['edus'])))
        print("{} CDUs".format(len(game['cdus'])))
        print("{} relations".format(len(game['relations'])))


        #Check CDUS
        cdu_components = []

        schema_ids = [cdu['schema_id'] for cdu in game['cdus']]

        for cdu in game['cdus']:
            if len(cdu['embedded_units']) < 2:
                cdu_components.append(cdu['schema_id'])

        #Count cdus in cdus
        if len(game['embedded_cdus']) > 0:
            print("{} CDUs contain CDUS:".format(len(game['embedded_cdus'])))
            for item in game['embedded_cdus']:
                print("CDU {} contains {}".format(item['parent_id'], item['child_id']))
        else:
            print("No CDUs containing CDUs.")
        print("---------------------")

        if len(cdu_components) == 0:
            print("All CDUs have two or more components")
        else:
            print("{} CDUs have less than two components. Printing to log.".format(len(cdu_components)))
            log_string += "CDUs with fewer than two elements: \n"
            components_string = '\n'.join(cdu_components)
            log_string += components_string
            log_string += '\n------------------------------------\n'

        print("----------------------")
        #Check CDU punctures
        cdu_punctures = []
        relation_targets = [(rel['y_id'], rel['relation_id']) for rel in game['relations']]
        relation_targets = dict(relation_targets)
        relation_sources = [(rel['relation_id'], rel['x_id']) for rel in game['relations']]
        relation_sources = dict(relation_sources)
        # if len(game['embedded_cdus']) > 1:
        #     child_parent = {}
        #     for item in game['embedded_cdus']:
        #         child_parent[item['child_id']] = item['parent_id']
        
        #possible_punctures = []
        for cdu in game['cdus']:
            #get all elements and check that any incoming links originate from another element
            elements = cdu['embedded_units']
            for element in elements:
                if element in relation_targets.keys():
                    #check that source of relation is also in CDU, or is the CDU itself
                    source = relation_sources[relation_targets[element]]
                    if source not in elements and source != cdu['schema_id']:
                        #keep track of the schema id and the component that's punctured
                        cdu_punctures.append((cdu['schema_id'], element))
            #   WIP!!          #it could be a relation coming from another CDU that is co-embeded in the CDU
            #             possible_punctures.append(element)
            # #check for other embedded CDU situations
            # if len(possible_punctures) > 1:
            #     if len(game['embedded_cdus']) > 1 & cdu['schema_id'] in child_parent.keys():
            #         #check if cdu is child of another CDU then check its children
            #         parent_cdu = child_parent[cdu['schema_id']]
        
        if len(cdu_punctures) == 0:
            print("No CDU punctures")
        else:
            print("{} CDU punctures found. Printing to log.".format(len(cdu_punctures)))
            log_string += "elements that form CDU punctures: \n"
            for puncture in cdu_punctures:
                print("Schema: {}, element: {}".format(puncture[0], puncture[1]))
                log_string += "Schema: " + puncture[0] + " unit: " + puncture[1] + "\n"
            log_string += '\n------------------------------------\n'

        #Check that every EDU and CDU has an incoming relation unless is is a member of a CDU
        all_elements = [edu['unit_id'] for edu in game['edus'][1:]]
        all_elements.extend(schema_ids)

        els = set(all_elements)
        targs = set(relation_targets.keys())
        not_targs = els.difference(targs)
        if len(not_targs) != 0:
            ##if difference is not empty, check against all cdu components
            emb_els = []
            for cdu in game['cdus']:
                emb_els.extend(cdu['embedded_units'])
            ee = set(emb_els)
            not_embs = not_targs.difference(ee)
            if len(not_embs) > 0:
                print("{} elements don't have incoming links:".format(len(not_embs)))
                log_string += "elements that don't have incoming links: \n"
                for e in list(not_embs):
                    print("{}".format(e))
                    log_string += e + "\n"
                log_string += '\n------------------------------------\n'
            else:
                print("All (non-dialogue initial) elements have at least one incoming link.")

        #print out logs
        if len(log_string) > 2:
            with open(log_path + '/' + game_name + '.txt', 'w') as text_file:
                    text_file.write(log_string)
            print("Logs written for {} \n\n".format(game_name))
        else:
            games_pass.append(game_name)

print("finished")
for g in games_pass:
    print("{} is ok".format(g))






