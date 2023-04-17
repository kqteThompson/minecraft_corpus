"""
functions for basic game stats called in stats.py
"""
from collections import defaultdict
from statistics import mode

#number of games
#number of turns
#breakdown of turns

#number of multi-parent edus
#breakdown of multi-parent edus

def num_games(data):
    games = [d['id'] for d in data]
    return len(games)


def relations(data):
    #reformat relation data
    # rels = {}
    # backwards = {}
    # for d in data:
    #     count = defaultdict(list)
    #     back_count = defaultdict(list)
    #     for r in d['relations']:
    #         length = abs(r['y'] - r['x'])
    #         if r['x'] > r['y']:
    #             back_count[r['type']].append(length)
    #         count[r['type']].append(length)
    #     rels[d['id']] = count
    #     backwards[d['id']] = back_count
    # print(backwards)
    # rel_types = defaultdict(list)
    # for r in rels:
    #     print(r)
    #     k = r.key()
    #     for i in r[k]:
    #         rel_types[i]+= r[k][i]
    # for r in rel_types:
    #     rt = r.key()
    #     print('{} : {} instances'.format(rt, len(r[rt])))
    #     print('{} max length : {} min length : {} mode'.format(max(r[rt]), min(r[rt]), 'bleh'))
    # #for each relation type, get 
    #max number in each game


    rels_all = defaultdict(list)
    backwards = defaultdict(list)
    for d in data:
        for rel in d['relations']:
            length = abs(rel['y'] - rel['x'])
            if rel['x'] > rel['y']:
                backwards[rel['type']].append(length)
            rels_all[rel['type']].append(length)
    print('------ALL RELATIONS-----\n')
    for r in rels_all.items():
        print('{} : {} instances'.format(r[0], len(r[1])))
        print('\n max length : {} \n min length : {} \n mode : {} \n\n'.format(max(r[1]), min(r[1]), mode(r[1])))
    print('------BACKWARDS-----\n')
    for b in backwards.items(): 
        print('{} : {} instances'.format(b[0], len(b[1])))
        print('\n max length : {} \n min length : {} \n mode : {} \n\n'.format(max(b[1]), min(b[1]), mode(b[1])))

    return None

def corrections(data):
    l = []
    z = []
    for d in data:
        corrs = 0
        for r in d['relations']:
            if r['type'] == 'Correction':
                corrs += 1
        if corrs > 0:
            l.append((corrs, d['id']))
            corrs = 0
        else:
            z.append(d['id'])

    l = sorted(l, key = lambda x: x[0])
    for g in l:
        print('{} corrections {}'.format(g[0], g[1]))
    print('----{} games with no corrections----'.format(len(z)))
    for g in z:
        print(g)
    return None

def parents(data):
    return None

    