# minecraft corpus annotation scripts


## to create GLOZZ files from Minecraft text files. 


## to create json files from games in GLOZZ xml & txt format
1. asdfasdf
2. sadfsadf

## to run a sanity check on games
1. Create a json from aa files --> /glozz_to_json/create_json.py
If there are any relation issues (ie a relation is missing an endpoint), 
it will give a warning and skip a file. 
Make sure to check the file manually in glozz before re-running this step.
2. Then run /sanity_checks/perform_checks.py
Then look at logs to see which games have issues
3. 

## to flatten CDUs in games.json


## to create BERT data from games.json

## How to flatten and squish an annotated GLOZZ file for BERT
1. Convert glozz file to json --> /glozz_to_json/create_json.py
2. Flatten and squish json -->  /flatten/squish_flatten_cdus.py
3. Convert to BERT format --> /bert/bert_format_annotated.py

## How to convert BERT predictions to BERT json format
1. asfsedf NB sometimes speaker for builder actions is "builder"

## How to put BERT formatted json into GLOZZ format
1. /bert_to_glozz/applygen.py






