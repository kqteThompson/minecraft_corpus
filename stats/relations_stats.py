"""
functions for basic game stats called in stats.py
"""
from collections import defaultdict, Counter
from statistics import mean, median, mode
import pandas
import numpy 
import matplotlib.pyplot as plt

#number of games
#number of turns
#breakdown of turns

#number of multi-parent edus
#breakdown of multi-parent edus

labels_map = {'Comment': 0, 'Contrast': 1, 'Correction': 2, 'Question-answer_pair': 3, 'Parallel': 4, 'Acknowledgement': 5,
            'Elaboration': 6, 'Clarification_question': 7, 'Conditional': 8, 'Continuation': 9, 'Result': 10, 'Explanation': 11,
            'Q-Elab': 12, 'Alternation': 13, 'Narration': 14, 'Confirmation_question': 15, 'Sequence' : 17, 'Background': 18}

reverse_map = {0: 'Comment', 1:'Contrast', 2:'Correction', 3:'QAP', 4:'Parallel', 5:'Acknowledgement',
            6:'Elaboration', 7:'Clarification_question', 8:'Conditional', 9:'Continuation', 10:'Result', 11:'Explanation',
            12:'Q-Elab', 13:'Alternation', 14:'Narration', 15:'Conf-Q', 17:'Sequence', 18:'Background'}

def num_games(data):
    games = [len(d['edus']) for d in data]
    num_games = len(games)
    print('Total games: {}'.format(num_games))

    dist = Counter(games)
    # labels, values = zip(*dist.items())
    # indexes = numpy.arange(len(labels))
    # width = 1

    # plt.bar(indexes, values, width)
    # plt.xticks(indexes + width * 0.5, labels)
    # plt.show()

    print('Game len | Number')
    dist = Counter(games)
    for k in sorted(dist.keys()):
        print('{} ----- {}'.format(k, dist[k]))
    print('Mean : ', float(f'{mean(games):.1f}'))
    print('Median : {} \n Mode: {} \n Min: {} \n Max: {}'.format(median(games), mode(games), min(games), max(games)))
    return None

def contains_number(string):
    return any(char.isdigit() for char in string)

def is_nl(edu):
    """
    if every word in alphanumeric
    """
    nl = 1
    words = edu.split(' ')
    # print(words)
    for word in [w for w in words if w != '']:
        if not contains_number(word):
            nl = 0
            break
    return nl

def edu_types_by_relation(data):
    """
    0 = NL move
    1 = L move
    """
    rels_forward = defaultdict(list)
    backwards = defaultdict(list)
    for game in data:
        edus = game['edus']
        edu_types = []
        #a list of edus as types...the location of the edu will be its index in the list
        for edu in edus:
            if edu['speaker'] == 'Builder' and is_nl(edu['text']):
                edu_types.append(0)
            else:
                edu_types.append(1)
        for rel in game['relations']:
            if int(rel['x']) > int(rel['y']):
                backwards[rel['type']].append((edu_types[int(rel['y'])], edu_types[int(rel['x'])]))
            else:
                rels_forward[rel['type']].append((edu_types[int(rel['x'])], edu_types[int(rel['y'])]))
        #get a dict with relation types as keys and list of tuples for endpoint type pairs 
    # print(rels_forward.keys())
    # print(backwards['Comment'])
    #reformat dict for printing
    labels = []
    data = []
    head = ['Lin-Lin', 'Lin-NL', 'NL-Lin', 'NL-NL', 'Total']
    for k in rels_forward.keys():
        labels.append(k)
        counts = Counter(rels_forward[k])
        data.append([counts[(1,1)], counts[(1,0)], counts[(0,1)], counts[(0,0)], len(rels_forward[k])])

    print('Forward Relations')
    print('                                         ')
    print(pandas.DataFrame(data, labels, head))
    print('                                         ')
        
    labels = []
    data = []
    head = ['Lin-Lin', 'Lin-NL', 'NL-Lin', 'NL-NL', 'Total']
    for k in backwards.keys():
        labels.append(k)
        counts = Counter(backwards[k])
        data.append([counts[(1,1)], counts[(1,0)], counts[(0,1)], counts[(0,0)], len(backwards[k])])

    print('Backwards Relations')
    print('                                         ')
    print(pandas.DataFrame(data, labels, head))
    print('                                         ')

    return None


def relations(data, maxlen):
    cutoff = maxlen[0]
    rels_all = defaultdict(list)
    backwards = defaultdict(list)
    for game in data:
        for rel in game['relations']:
            length = abs(rel['y'] - rel['x'])
            
            if rel['x'] > rel['y']:
                backwards[rel['type']].append(length)
            else:
                rels_all[rel['type']].append(length)
    #get counts for each type

    head = ['Total']
    labels = []
    data = []
    len_range = [i for i in range(1,cutoff+1)]

    head.extend([str(l) for l in len_range])
    head.extend(['num over', 'max'])

    for k in rels_all.keys():
        labels.append(k)
        under = Counter([r for r in rels_all[k] if r <= cutoff])
        over = [r for r in rels_all[k] if r > cutoff]
        d = []
        d.append(len(rels_all[k]))
        for n in len_range:
            d.append(under[n])
        d.append(len(over))
        d.append(max(rels_all[k]))
        data.append(d)

    print('Forward Relations')
    print('                                         ')
    print(pandas.DataFrame(data, labels, head))
    print('                                          ')
    
    labels = []
    data = []
    for k in backwards.keys():
        labels.append(k)
        under = Counter([r for r in backwards[k] if r <= cutoff])
        over = [r for r in backwards[k] if r > cutoff]
        d = []
        d.append(len(backwards[k]))
        for n in len_range:
            d.append(under[n])
        d.append(len(over))
        d.append(max(backwards[k]))
        data.append(d)

    print('Backwards Relations')
    print('                                         ')
    print(pandas.DataFrame(data, labels, head))
    print('                                          ')

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

def multi_parents(data):
    totals = []
    for d in data:
        cnt = defaultdict(list)
        for rel in d['relations']:
            cnt[rel['y']].append(labels_map[rel['type']])
        totals.extend([c[1] for c in cnt.items() if len(c[1]) > 1])
    #so now should have totals list that is all the relation types for multi parent edus
    total_counts = defaultdict(list)
    all_lengths = []
    for t in totals:
        l = len(t)
        all_lengths.append(len(t)) #to figure out the range of lens
        for i in t:
            total_counts[i].append(l)
    #so now you have a dict with relation types as keys and multi parent nums as values
    head = list(set(all_lengths))
    head.sort()
    labels = []
    data = []
    for k in total_counts.keys():
        labels.append(reverse_map[k])
        counts = Counter(total_counts[k])
        data.append([counts[n] for n in head])

    print('Relations in multi-parent edus')
    print('                                         ')
    print(pandas.DataFrame(data, labels, head))
    print('                                         ')   
    return None

def parents(data):
    #find all edus with more than one parent
    #return total number, then max length of relation
    totals = []
    more_than_2 = []
    more_than_2_totals = []
    for d in data:
        cnt = defaultdict(list)
        for rel in d['relations']:
            cnt[rel['y']].append(abs(rel['y']-rel['x']))
        for item in cnt.items():
            if len(item[1]) > 1:
                totals.append(max(item[1]))
                more_than_2.append(len(item[1]))
            if len(item[1]) > 2:
                more_than_2_totals.append(max(item[1]))
    print('{} instances of multi-parent edus'.format(len(totals))) 
    print('{} relations longer than 10 among 2 or more parents'.format(len([t for t in totals if t > 10])))
    print('{} relations longer than 10 among 3 or more parents'.format(len([t for t in more_than_2_totals if t > 10])))

    # counts = Counter(totals)   
    # for item in counts.items():
    #     print('{} : {}\n'.format(item[0], item[1]))   

    print('{} edus with more than 1 parents:'.format(len(more_than_2)))
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
            print('total number of relations <= {}: {} // {} of total relations'.format(n, rel_rels, round(rel_rels/all_rels, 4)))
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
            total = 0
            for k in sorted(lens.keys()):
                #order by ascending length 
                print('length: {}, number: {}'.format(k, lens[k]))
                total += lens[k]
            print('TOTAL : {}'.format(total))
            # for l in lens.items():
            #     print('length: {}, number: {}'.format(l[0], l[1]))
    return None

def rels_within_cutoff(data, length):
    totals = defaultdict(list)
    for d in data:
        for rel in d['relations']:
            totals[rel['type']].append(abs(rel['x']-rel['y']))

    return None
    