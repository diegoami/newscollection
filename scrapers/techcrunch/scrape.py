"""
Please, before executing the code, refer to the config file `config.yml` on
the root folder and the request headers on `src/header.json`.

You can set the following variables on your configuration file:

    -> Section: sections to be scraped
    -> MinPage: starting page to start scraping
    -> MaxPage: last page that will be scraped
    -> Request > Timeout: maximum time to wait for a HTTP response
    -> SaveBatch: number of processed items required to save results
    -> SleepTime: time the program will stop before making another request (
        please use values above or equal to 2.0 seconds to be as friendly as
        possible).

Make your scraper identifiable by setting a proper `user-agent` (your email is a
good choice) value on the header file.
"""
__author__ = 'Thiago Balbo'
__email__ = 'thiago.dbalbo@gmail.com'
__version__ = '1.0'

import requests
import lxml.html
import yaml, time, sys, json, csv, os
import datetime
import json

config = yaml.safe_load(open('config.yml'))
print(config)


def console_log(message):
    """
    Print a message to the terminal with the datetime at the beginning.

    :param message: The message to be print.
    """
    ctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[{}]'.format(ctime), message)




class Scraper:
    """
    Scraper implements base methods to scrape and parse data from an URL.
    """
    def __init__(self, headers):
        self.headers = headers


    def scrape(self, url, referer=None):
        """
        Make a GET request to a URL.

        :param url: url to be requested
        :param referer: the requests' referer
        :returns: requests' response.
        """
        if referer:
            self._add_referer(referer)

        response = requests.get(url, timeout=self._timeout,
                            headers=self.headers)

        return response


    def parse(self, raw_data):
        """
        Parse data from a raw string to a formated tree object.

        :param raw_data: a string to be parsed (will be the html page as string)
        :returns: the parsed string as a lxml.html tree object
        """
        root = lxml.html.fromstring(raw_data)
        return root


    def _add_referer(self, referer):
        """
        Add referer to the request header.

        :param referer: the referer to be added.
        """
        self.headers['referer'] = referer



class TechCrunchScraper(Scraper):
    """
    This is the main class used to scrape posts from the TechCrunch website.
    It will execute several methods. The process includes:

    1. Get all links for a custom page and section and yield them
    2. For each post, scrape its content
    3. Save the results ocasionally in a json file
    4. Repeat 1-3 until all config conditions (pages and sections) are
    satisfied.
    """
    def __init__(self):
        self.posts = []

        self.url = config['URL']
        self.sections = config['Section']
        self.page = config['Page']
        self.max_page = config['MaxPage']
        self.min_page = config['MinPage']
        self.sleep_time = config['SleepTime']
        self.max_links = config['MaxLinks']

        self.links_filename = config.get('LinksFilename')
        self.posts_filename = config.get('PostsFilename')
        self.save_batch = config.get('SaveBatch')
        self.input_file_name = config.get('InputFilename')
        self.output_file_name = config.get('OutputFilename')

        headers_filename = config.get('Request')['HeaderFilename']
        with open(headers_filename, 'r') as f:
            headers = json.load(f).get('Items')
        super().__init__(headers)

        self._timeout = config.get('Request')['Timeout']

        print(self.sections)
        self.load_old_links()


    def is_link_saved(self, url):
        return any([url == post['url'] for post in self.posts ])

    def load_old_links(self):
        if os.path.isfile(self.input_file_name):
            with open(self.input_file_name, 'r') as f:
                jsmap = json.load(f)
                self.posts = jsmap["posts"]




    def _get_page_links(self, url, section, referer=None):
        """
        Get the data from the section page. Includes posts' URL, category, id
        and section.

        :param url: the section url to be scraped
        :param section: the section that is being scraped
        :param referer: the referer to add to the request header
        :returns: a list of dictionaries containig the metadata of all posts
            in the page.
        """
        links = []

        resp = self.scrape(url, referer=referer)
        html_doc = self.parse(resp.text)

        elements = html_doc.cssselect('ul.river > li')
        for elem in elements:
            try:
                cat_obj = elem.cssselect('div.tags span')[0]
                category = cat_obj.text_content()
            except:
                category = ''

            link = {
                'id': elem.get('id'),
                'permalink': elem.get('data-permalink'),
                'category': category,
                'section': section
            }

            links.append(link)

        return links


    def get_links(self):
        """
        Controller to get the links from the website sections

        :returns: yield a dicionary containing the url and other metadata of
            the post.
        """
        for page in range(self.min_page, self.max_page+1):
            console_log('Page: {}'.format(page))

            for section in self.sections:
                console_log('Section: {}'.format(section))

                url = self.url + section + self.page.format(num=page)

                try:
                    links = self._get_page_links(url, section)

                    for link in links:
                        yield link

                except Exception as e:
                    print(e)
                    time.sleep(0.5) # so you have time to ctrl-C
                    continue


    def scrape_post(self, link):
        """
        Scrape the content from the post.

        :param link: a dictionary containing the url to be scraped and other
            metadata from the post.
        :returns: post content as a dictionary
        """
        resp = self.scrape(link.get('permalink'))
        html_doc = self.parse(resp.text)

        images = html_doc.cssselect('div.article-entry.text > img')
        if len(images) > 0:
            image_src = images[0].get('src')
        else:
            image_src = ""
        paragraphs = html_doc.cssselect('div.article-entry.text > p')
        content = []
        for paragraph in paragraphs:
            content.append(paragraph.text_content())

        post_info = html_doc.cssselect('div.title-left')[0]
        date = post_info.cssselect('div.byline > time')[0].get('datetime')

        authors = post_info.cssselect('div.byline > a')
        by = []
        for author in authors:
            by.append(author.text_content())


        post_tags = html_doc.cssselect('div.accordion.recirc-accordion li')
        tags, topics = [], []
        for tag in post_tags:
            try:
                tag_id = tag.get('id').replace('tc-accordion-item-','')
                tag_content, tag_type = tag_id.rsplit('-', 1)
                if tag_type == 'tag':
                    tags.append(tag_content)
                elif tag_type == 'topic':
                    topics.append(tag_content)
            except:
                pass

        title = html_doc.cssselect('header.article-header.page-title > h1')[0]
        title_text = title.text_content()

        post_metadata = {
            'id': link.get('id'),
            'url': link.get('permalink'),
            'title': title_text,
            'section': link.get('section'),
            'category': link.get('category'),
            'tags': ','.join(tags),
            'topics': ','.join(topics),
            'img_src': image_src,
            'text': '\n'.join(content),
            'date': date,
            'authors': ','.join(by)
        }

        return post_metadata


    def scrape_post_flow(self, link):
        """
        Controller to call the function that will actually scrape the HTML
        content and append items to memory.

        :param link: the link to be scraped
        """
        console_log('Scraping post {}'.format(link.get('permalink')))

        try:
            if not self.is_link_saved(link['permalink']):
                post_metadata = self.scrape_post(link)
                self.posts.append(post_metadata)
            else:
                print("Skipping "+link['permalink'])
        except Exception as e:
            print(e)
            time.sleep(0.5) # so you have time to ctrl-C


    def save(self, output, filename):
        """
        Save a list of dictionaries into a csv file.

        :param output: a list of dictionaries to be saved
        :param filename: filename to save the data
        """
        with open(self.output_file_name, 'w',encoding='UTF-8') as f:
            mmap = {"posts": self.posts}
            json.dump(mmap , f, ensure_ascii=False)

    def save_flow(self, num, last=False):
        """
        Test conditions to check wether or not to save the data.

        :param num: the number of scraped urls until now
        :param last: if this will be the last time this method will be called
        """
        ct = datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')
        if (num % self.save_batch == 0 and self.posts) or (last and self.posts):
            console_log('Saving posts...')
            path = self.posts_filename.rsplit('/', 1)[0]
            if not os.path.exists(path):
                os.system('mkdir -p {}'.format(path))
            self.save(self.posts, self.posts_filename.format(dt=ct))



    def run(self):
        scraped_urls = 0
        links = self.get_links()
        while 1:
            if scraped_urls % 10 == 0:
                console_log('Scraped URLs: {}'.format(scraped_urls))

            try:
                self.scrape_post_flow(next(links))
            except StopIteration:
                self.save_flow(scraped_urls, last=True)
                sys.exit()

            scraped_urls += 1
            self.save_flow(scraped_urls)

            time.sleep(self.sleep_time)
            if (scraped_urls > self.max_links):
                print("Retrieved {} links : exiting ".format(scraped_urls ))
                self.save_flow(scraped_urls, last=True)
                sys.exit()



if __name__ == '__main__':
    s = TechCrunchScraper()
    s.run()
