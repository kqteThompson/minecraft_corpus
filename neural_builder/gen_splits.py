
def get_splits(orig_splits, snips):
    """
    takes a dict of splits used in original BAP experiments
    and a list of split games
    and returns a new set of splits such that all the snippets are used for 
    training.
    NB: new val games are not randomized
    """
    snip_splits = {}
    snip_splits['test'] = orig_splits['test']
    new_train = orig_splits['train']
    new_train.extend(orig_splits['val'])
    total = len(new_train)
    val_prop = round(total * .1)
    val_cand = [e for e in new_train if e not in snips]
    new_val = val_cand[:val_prop+1]
    new_train = [e for e in new_train if e not in new_val]
    snip_splits['train'] = new_train
    snip_splits['val'] = new_val
    return snip_splits