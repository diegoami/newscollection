# TECH NEWS AGGREGATOR


## General purpose

The general idea is to build a technology news portal aggregating tech news from several sources and draw conclusions from them

* find articles discussing the same news item as a provided text, but from a different source
* get a different angle about a specific news item or topic from a different source
* find controversial news in a period of time, that have been treated seperately from several sources.


## Dataset


Currently the dataset includes technical articles that have been published between 01/01/2017 and 30/10/2017 on following tech sources

* [Techcrunch](http://www.techcrunch.com)
* [The Verge](http://www.theverge.com)
* [The next web](http://www.thenextweb.com)
* [Venture beat](http://www.venturebeat.com)
* [Ars Technica](http://www.arstechnica.com)
* [Tech Republic](http://www.techrepublic.com)


So far it is about 45.000 articles.

## Currently deployed

### Prototype

A prototype is currently accessible [on this site](http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com:8080).

### Similar articles and conteroversial topics

You can find "controversial" topics in the datbase. [You can browse through the articles](http://18.194.147.93:8080/duplicates/0') that have been paired because the system considers it likely that they are talking about the same topic, possibly under a different slant.

[You can help validate this pairings here](http://18.194.147.93:8080/randomrelated).


### Finding Related articles

The idea behind this is that after you find an article on the web, you would want to find another article talking about the same topic from a different source.

This works also as a recommandation system, because it should find articles talking about related topics.

[You can copy the text of a technical article into this text page](http://18.194.147.93:8080/search)  and find similar articles in the dataset, possibly limiting the search in a date interval.

Alternatively, you can see how articles in the database related to each other [entering the url of an article in this page](http://ec2-35-156-126-138.eu-central-1.compute.amazonaws.com:8080/search_url).


## Technologys used

I am still in the exploring phase as to what technology I should use. So far I built the prototype using Gensim in connection with Tfidf / BoW (first approach) and Doc2Vec. The results are already decent but it seems that there is great room for improvement.

## Validation

I have included the possibility to let users [give feedback](), whether articles actually are about the same story, or at least related. If enough data is gathered, other approaches to train models will be used, such as neural networks.

## Possible developments

I am also considering following developments

* Work as a recommender system - find articles whose topics is related to the one you have selected
  * at first these recommendations would be stateless, but it can be extended to remember previous user choices

* Categorize articles / texts based on tags and authors of articles in the database, to try and help to get recommendations

* Implement a real smart search engine over the database of technical articles

* Summarize articles

* Finds differences about articles describing the same story

* Trying to find out which one is more interesting
