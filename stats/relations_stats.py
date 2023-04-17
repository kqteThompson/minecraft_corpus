"""
functions for basic game stats called in stats.py
"""
from collections import defaultdict, Counter
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
    rels_all = defaultdict(list)
    backwards = defaultdict(list)
    total = []
    for d in data:
        for rel in d['relations']:
            length = abs(rel['y'] - rel['x'])
            total.append(length)
            if rel['x'] > rel['y']:
                backwards[rel['type']].append(length)
            rels_all[rel['type']].append(length)
    print('total number of relations: {}'.format(len(total)))
    print('Longest relation: length {}'.format(max(total)))
    print('------ALL RELATIONS-----\n')
    for r in rels_all.items():
        print('{} : {} instances'.format(r[0], len(r[1])))
        print('\n max length : {} \n min length : {} \n mode : {} \n'.format(max(r[1]), min(r[1]), mode(r[1])))
    print('------BACKWARDS-----\n')
    for b in backwards.items(): 
        print('{} : {} instances'.format(b[0], len(b[1])))
        print('\n max length : {} \n min length : {} \n mode : {} \n'.format(max(b[1]), min(b[1]), mode(b[1])))

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
    #find all edus with more than one parent
    #return total number, then max length of relation
    totals = []
    more_than_2 = []
    for d in data:
        cnt = defaultdict(list)
        for rel in d['relations']:
            cnt[rel['y']].append(rel['x'])
        for item in cnt.items():
            if len(item[1]) > 1:
                totals.append(max(item[1]))
                more_than_2.append(len(item[1]))
    print('{} instances of multi-parent edus'.format(len(totals))) 
    print('{} relations longer than 10'.format(len([t for t in totals if t > 10])))

    # counts = Counter(totals)   
    # for item in counts.items():
    #     print('{} : {}\n'.format(item[0], item[1]))   

    print('{} edus with more than 2 parents:'.format(len(more_than_2)))
    more_counts = Counter(more_than_2)
    for item in more_counts.items():
        print('{} : {}'.format(item[0], item[1])) 

    return None

def get_cands(data, num):
    totals = []
    for d in data:
        edus = len(d['edus'])
        cutoff = edus - num
        h1 = cutoff * num
        h2 = (num * (num-1))/2
        totals.append(h1+h2)
    return totals

def candidates(data, num=None):
    rels = []
    for d in data:
        for r in d['relations']:
            rels.append(abs(r['x'] - r['y']))
    rel_lengths = Counter(rels)
    if num:
        all_rels = sum([c[1] for c in rel_lengths.items()])
        for n in num:
            totals = get_cands(data, n)
            print('Length of {}'.format(n))
            print('total candidates: {}'.format(sum(totals)))
            rel_rels = sum([c[1] for c in rel_lengths.items() if c[0]<= n])
            print('total number of relations <= {}: {} // {} of total'.format(n, rel_rels, round(rel_rels/all_rels, 4)))
    else:
        totals = []
        for d in data:
            edus = len(d['edus'])
            cands = ((edus-1) * edus)/2
            totals.append(cands)
        print('total candidates: {}'.format(sum(totals)))
        total_rels = sum([c[1] for c in rel_lengths.items()])
        print('total number of relations: {}'.format(total_rels))

    return None

def find_longest_rels(data, length):
    totals = defaultdict(list)
    for d in data:
        for rel in d['relations']:
            totals[rel['type']].append(abs(rel['x']-rel['y']))
    for t, c in totals.items():
        lens = Counter([i for i in c if i >= length[0]])
        if lens:
            print('----{}----'.format(t))
            for l in lens.items():
                print('length: {}, number: {}'.format(l[0], l[1]))
    return None
    