import os
import json
import argparse
import relations_stats

# --------------------------
# args
# --------------------------

arg_parser = argparse.ArgumentParser(description='generate minecraft games stats')
arg_parser.add_argument('json_file_name', metavar='CORPFILE', help='name of json file with games')
arg_parser.add_argument("--games", default=False, action='store_true', help='give num games') 
arg_parser.add_argument("--relations", default=False, action='store_true', help='asdfsdf')
arg_parser.add_argument("--parents", default=False, action='store_true', help='sadfasdf')
arg_parser.add_argument("--corrections", default=False, action='store_true', help='sadfasdf')

args = arg_parser.parse_args()

current_dir = os.getcwd()

##try to open json file and check turns 

json_path = current_dir + '/' + args.json_file_name

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
if args.relations:
    #return relation stats 
    #number of relations
    #breakdown of relation types
    #number of backwards relations
    relations_stats.relations(data)
if args.corrections:
    relations_stats.corrections(data)
