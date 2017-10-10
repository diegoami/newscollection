from . import url_to_filename
import os
import requests
import time

class Raw_Retriever:

    def __init__(self, iterator, raw_base_dir, exclusions):
        self.iterator = iterator
        self.raw_base_dir = raw_base_dir
        self.exclusions = exclusions


    def download_files(self):
        for url, v in self.iterator:
            basefilename = url_to_filename(url)
            filename = self.raw_base_dir + basefilename

            if not os.path.isfile(filename) and not any([x for x in self.exclusions if basefilename.startswith(x)]):
                headers = {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
                }
                r = requests.get(url, headers=headers)
                with (open(filename, 'w')) as f:
                    f.write(r.text)
                    print("Saved page: " + filename)
                    time.sleep(0.5)
            else:
                print("Skipping: " + filename)

