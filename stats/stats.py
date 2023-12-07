import os
import json
import argparse
import relations_stats

# --------------------------
# args
# --------------------------

arg_parser = argparse.ArgumentParser(description='generate minecraft games stats')
arg_parser.add_argument('json_file_name', metavar='CORPFILE', help='name of json file with games')
arg_parser.add_argument("--games", default=False, action='store_true', help='give num games and dist of game lengths') 
arg_parser.add_argument("--relations", default=False, action='store_true', help='asdfsdf')
arg_parser.add_argument("--parents", default=False, action='store_true', help='returns number of edus with >1 parent')
arg_parser.add_argument("--corrections", default=False, action='store_true', help='returns game and num correction relations')
arg_parser.add_argument("--candidates", default=False, action='store_true', help='returns number of candidates for a particular cutoff')
arg_parser.add_argument("--num", type=int, nargs='+', help='specify particular cutoff for --candidates or --relations')
arg_parser.add_argument("--undersample", type=int, nargs='+', help='specify number of 0 cands to drop if wanting to keep this balance')
arg_parser.add_argument("--longest_rels", type=int, nargs=1, help='returns a list of relation types with len >= num')
arg_parser.add_argument("--edu_types", default=False, action='store_true', help='returns a list of relation types edu type breakdown')
arg_parser.add_argument("--multiparents", default=False, action='store_true', help='rel types for >1 parent edus')
arg_parser.add_argument("--narrations", default=False, action='store_true', help='asdfsdf')
arg_parser.add_argument("--last", default=False, action='store_true', help='scores for last')

arg_parser.add_argument("--prep_outputs", default=False, action='store_true', help='changes field names on bert output')
arg_parser.add_argument("--save_name", type=str, nargs='+', help='specify new file name')

args = arg_parser.parse_args()

current_dir = os.getcwd()

##try to open json file and check turns 

json_path = current_dir + '/jsons/' + args.json_file_name

try:
    with open(json_path, 'r') as f: 
        obj = f.read()
        data = json.loads(obj)
except IOError:
    print('cannot open json file ' + json_path)


output_path = current_dir + '/stats.txt'


if args.games:
    #count number of games
    num_games = relations_stats.num_games(data)
    print('{} games'.format(num_games))
if args.narrations:
    relations_stats.narrations(data)
if args.relations:
    #return relation stats 
    #number of relations
    #breakdown of relation types
    #number of backwards relations
    if args.num:
        relations_stats.relations(data, args.num)
    else:
        print('Need to specify cutoff distance in --num')
if args.corrections:
    relations_stats.corrections(data)
if args.parents:
    relations_stats.parents(data)
if args.candidates:
    if args.num:
        relations_stats.candidates(data, args.num)
    else:
        relations_stats.candidates(data)
if args.last:
    if args.num:
        relations_stats.last(data, args.num)
    else:
        relations_stats.last(data)
if args.longest_rels:
    relations_stats.find_longest_rels(data, args.longest_rels)
if args.edu_types:
    relations_stats.edu_types_by_relation(data)
if args.multiparents:
    relations_stats.multi_parents(data)
if args.prep_outputs:
    new = relations_stats.prep(data)
    with open(current_dir + '/jsons/' + args.save_name[0] + '_prep.json', 'w') as outfile:
        json.dump(new, outfile)
    print('new json saved!')


