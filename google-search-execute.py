import yaml
config = yaml.safe_load(open('config.yml'))
google_config_file = config["google_key_file"]
google_config      = yaml.safe_load(open(google_config_file))
api_key            = google_config['developerKey']

import json

from technews_nlp_aggregator.scraping.google_search_wrapper import Command
from technews_nlp_aggregator.scraping.google_search_wrapper import create_google_service


def execute_command_file(command_file):
    print("Executing command_file={}".format(command_file))
    with open(command_file, 'r') as f:
        commands = json.load(f)
        execute_commands(commands)
        with open(command_file, 'w') as fw:
            json.dump(commands, fw, ensure_ascii=False)

def execute_commands(commands):
    outputdir = config['search_results_dir']

    for command in commands:
        google_service = create_google_service(api_key)
        command_obj = Command(google_service,command, outputdir)
        command_obj.execute_command()

import glob
gcmds = glob.glob(config['commands_pattern'])
for gcmd in gcmds:
    execute_command_file(command_file=gcmd)


