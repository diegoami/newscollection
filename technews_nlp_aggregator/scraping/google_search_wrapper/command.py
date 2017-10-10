
import json
from datetime import datetime
import time

class Command:

    def __init__(self, service, command, outputdir):
        self.service = service
        self.command = command
        self.outputdir = outputdir

    def execute_command(self):
        if self.command['executed'] == 0:

            query_params = self.command['query_params']
            if ("dayrange" in self.command):
                drange_str = self.command['dayrange']
                drange_r = list(map(int, drange_str.split(',')))
                for dr in range(drange_r[0], drange_r[1]+1):
                    query_param_day = dict(query_params )
                    query_param_day["q"] = query_params["q"]+("0" if dr <= 9 and not "nopad" in self.command else "") + str(dr)+"/"
                    self.extract_for_day(query_param_day)
            else:
                self.extract_for_day(query_params )
            self.command['executed'] = 1
        else:
            print("Already executed: "+str(self.command))

    def extract_for_day(self,query_params ):
        range_r = (1, 101)
        if "range" in self.command:
            ranges_str = self.command['range']
            range_r = list(map(int, ranges_str.split(',')))
        self.retrieve_search_result(range_r, query_params )

    def retrieve_search_result(self, range_r,query_params ):
        for r in range(range_r[0], range_r[1], 10):
            query_loop = dict(query_params)
            query_loop["start"] = r
            print(query_loop)
            query_result = self.save_search_result(query_loop)
            total_results = int(query_result['searchInformation']['totalResults'])
            if (total_results < r + 10):
                print("Totalresults = {}, skipping".format(total_results))
                break;
            time.sleep(0.5)
        return self.command


    def save_search_result(self, query_loop):
        query_result = self.service.cse().list(**query_loop).execute()
        query_total = {'query_params': query_loop, 'query_result': query_result}
        filename = self.outputdir+"search_google_" + datetime.now().isoformat() + ".json"
        with open(filename, 'w' ) as f:
            print("Saving to "+filename)
            json.dump(query_total, f, ensure_ascii=False)
        return query_result
