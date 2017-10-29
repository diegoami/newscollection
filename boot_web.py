import sys
from technews_nlp_aggregator.web import *
app.application = Application()
app.run(debug=True,  use_reloader=False, host='0.0.0.0',port=8080)
