# minecraft corpus annotation scripts


## to create GLOZZ files from Minecraft text files. 
1. /text_to_glozz/apply_gen.py

## to create split text files from parser output
1. /conll_to_splits/con_to_text.py 

## to create json files from games in GLOZZ xml & txt format
1. asdfasdf
2. sadfsadf

## to run a sanity check on games
1. Create a json from aa files --> /glozz_to_json/create_json.py
If there are any relation issues (ie a relation is missing an endpoint), 
it will give a warning and skip a file. NB: this is usually because a relation has a relation as a
constituent.
Make sure to check the file manually in glozz before re-running this step.
2. Then run /sanity_checks/perform_checks.py  Then look at logs to see which games have issues

## to flatten CDUs in games.json


## to create BERT data from games.json
1. NB: always make sure that you order the EDUS by position number (they may be out of order from hand splits)

## How to flatten and squish an annotated GLOZZ file for BERT
1. Convert glozz file to json --> /glozz_to_json/create_json.py
2. Flatten and squish json -->  /flatten/squish_flatten_cdus.py (or squish_only.py if using flattened versions)
3. Convert to BERT format --> /bert/bert_format_annotated.py*
*to specify test/train splits, use bert/preprocess.py FIRST

## How to convert BERT predictions to BERT json format
1. asfsedf NB sometimes speaker for builder actions is "builder"

## How to put BERT formatted json into GLOZZ format
1. /bert_to_glozz/applygen.py


## STATS

1. Get relation counts by relation type & length. Ex: with distance >= 11
```
python3 stats.py DATA.json --longest_rels 11
```
2. Get number of candidates generated and relations for cutoff less than or equal to num. Ex: num == 10
```
python3 stats.py DATA.json --candidates --num 10
```
3. For each relation get relation type, num instances, min and max length for forwards and backwards relations
```
python3 stats.py DATA.json --relations
```
4. Get comparison tables for each relation type for distances 1-10. Shows gold, and bert outputs.
```
python3 bert_stats.py
```
5. Get number of edus with multiple parents
```
python3 stats.py DATA.json --parents
```



