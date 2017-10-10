import glob
import json

class Iterator:

    def __init__(self, gsearch_results_pattern):
        self.gsearch_results_pattern = gsearch_results_pattern

        self.alllinks = {}

    def load(self):
        gsearch_results = glob.glob(self.gsearch_results_pattern)
        for gsearch_result in gsearch_results:
            with open(gsearch_result, 'r') as f:
                js_result = json.load(f)
                if "query_result" in js_result:
                    query_result = js_result["query_result"]
                    if "items" in query_result:
                        items = query_result["items"]
                        for item in items:
                            self.alllinks[item["link"]] = item["title"]

    def __iter__(self):
        for k, v in self.alllinks.items():
            yield k, v