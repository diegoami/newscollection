
import yaml
from technews_nlp_aggregator.web import *

from werkzeug.contrib.fixers import ProxyFix



app.wsgi_app = ProxyFix(app.wsgi_app)

config = yaml.safe_load(open('config.yml'))

key_config = yaml.safe_load(open(config["key_file"]))

key_config.get("secret_key")
app.config['SECRET_KEY'] = key_config.get("secret_key")
#app.run(debug=True,  use_reloader=False, host='0.0.0.0',port=8080)
app.application = Application()
if __name__ == '__main__':

    app.run(debug=True,  use_reloader=False)