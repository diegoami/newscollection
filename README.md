# TECH NEWS AGGREGATOR

## Background

### General purpose

The general idea is to build a technology news portal aggregating tech news from several sources and draw conclusions from them

* find articles discussing the same news item as a provided text, but from a different source
* get a different angle about a specific news item or topic from a different source
* find controversial news in a period of time, that have been treated seperately from several sources.

## Possible development

I am also considering following developments

* Work as a recommender system - find articles whose topics is related to the one you have selected
  * at first these recommendations would be stateless, but it can be extended to remember previous user choices

* Categorize articles / texts based on tags and authors of articles in the database, to try and help to get recommendations

* Implement a real smart search engine over the database of technical articles

## Dataset


Currently the dataset includes all technical articles that have been published between 01/01/2017 and 04/10/2017 on following tech sources

* Techcrunch (http://www.techcrunch.com)
* The Verge  (http://www.theverge.com)
* The next web (http://www.thenextweb.com
* Venture beat (http://www.venturebeat.com)

I am planning to update models with articles as they are published and add the following sources

* Ars Technica (http://www.arstechnica.com)
* Engadget     (http://www.engadget.com)
* Mashable     (http://www.mashable.com/tech)
* Bgr          (http://www.bgr.com)

So far it is about 30.000 articles - my target is having a database of about 100.000 articles and keep it updated. I have already built a scraper for that, whose source can be found here : https://github.com/diegoami/newscollection-scraper

## Currently deployed

### Prototype

A prototype is currently accessible at http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com/newscollection/


### Finding Related articles

The idea behind this is that after you find an article on the web, you would want to find another article talking about the same topic from a different source.

This works also as a recommandation system, because it should find articles talking about related topics.


You can copy the text of a technical article into this text page : http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com/newscollection/search.html  and find similar articles in the dataset, possibly limiting the search in a date interval.

This comes in the form also of a Chrome plugin that can be downloaded from here: http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com/newscollection/js-plugin/tnaggregator-chrome-plugin.zip and installed manually under chrome://extensions. If the user selects the text of a tech article and clicks on the Chrome extension, a popup will appear showing the related articles that could be found in the database.

### Interesting articles

The second application is finding "controversial" topics in a date range. From the page http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com/newscollection/interesting.html you can select a date range and request to system to find topics that have been handled in several articles from different sources in this period. **This is still slow and needs improvement**

## Technologys used

I am still in the exploring phase as to what technology I should use. So far I built the prototype using Gensim in connection with Tfidf / BoW (first approach) and Doc2Vec. The results are already decent but it seems that there is great room for improvement. In particular:

* Tfidf/BoW seems to be very slow but it comes probably also from a suboptimal implementation of my part
* Doc2vec's results are very misleading for short sentences and short articles, as the length of an article seems to be one of the main features to decide whether articles are similar

## Issues

* I am looking for ways to include other features to improve the score of similarity between two articles, apart from the text itself. In particular

  * Articles published around the same date are more likely to be related
  * So are articles having similar tags and from the same author and source

* On the other hand, when wishing to show articles about the same topic from different sources, I would want to penalize articles from the same source or author, as I am looking for a different angle.

* I am also striving to be able to limit search only on a subset of the dataset, (especially date) even after having trained the models on all of the articles.

* The update of articles in the database is still not automatized





