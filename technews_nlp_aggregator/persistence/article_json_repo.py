from .article_repo import ArticleRepo
import json
import os
import os.path

class ArticleJsonRepo(ArticleRepo):
    def __init__(self, link_file, parsed_base_dir):
        self.link_file = link_file
        self.parsed_base_dir = parsed_base_dir
        self.link_json = {}

    def load_articles(self):
        if (os.path.isfile(self.link_file)):
            with open(self.link_file, 'r') as f:
                self.link_json = json.load(f)


    def save_articles(self):
        with open(self.link_file, 'w') as g:
            json.dump(self.link_json, g, ensure_ascii=False)


    def url_exists(self, url):
        return url in self.link_json




    def set_url_information(self, url, to_add):
        self.link_json[url] = to_add


    def file_name_exists(self, filename):
        return os.path.isfile(self.parsed_base_dir  + filename)


    def save_text_to_file(self, filename, title, text):
        text_filename =  self.parsed_base_dir  + filename
        print("Writing file : " + text_filename)

        with open(text_filename, 'w') as fw:
            fw.write(title + '.\n')
            fw.write(text + '\n')


    def load_text_from_file(self, filename):
        if (self.file_name_exists(filename)):
            text_filename = self.parsed_base_dir + filename
            with open(text_filename, 'r') as fr:
                lines = fr.readlines()
                title = lines[0]
                text = "".join(lines[1:])
            return title, text
        else:
            return None, None

    def __iter__(self):
        for k,v in self.link_json.items():
            yield k, v

