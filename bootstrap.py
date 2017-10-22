import sys

from todiscard.rest.tn_service import *

sys.path.append('.')

sys.path.append('technews_nlp_aggregator')
app.run(debug=True, host='0.0.0.0',port=8080)
