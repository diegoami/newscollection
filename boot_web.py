
import yaml
from technews_nlp_aggregator.web import *
from technews_nlp_aggregator import Application
import argparse

from werkzeug.contrib.fixers import ProxyFix
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


app.wsgi_app = ProxyFix(app.wsgi_app)

config = yaml.safe_load(open('config.yml'))
parser = argparse.ArgumentParser()
parser.add_argument('--rootDir', help='since when')
args = parser.parse_args()
if args.rootDir is not None:
    config["root_dir"] = args.rootDir
key_config = yaml.safe_load(open(config["root_dir"]+config["key_file"]))

key_config.get("secret_key")
app.config['SECRET_KEY'] = key_config.get("secret_key")
#app.run(debug=True,  use_reloader=False, host='0.0.0.0',port=8080)
app.application = Application(config)
if __name__ == '__main__':

    app.run(debug=True,  use_reloader=False , port=8081)