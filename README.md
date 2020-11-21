# TECH NEWS AGGREGATOR


## General purpose

The idea is to build a technology news portal aggregating tech news from several sources and draw conclusions from them

* find articles discussing the same news item as a provided text, but from a different source
* get a different angle about a specific news item or topic from a different source
* find controversial news in a period of time, that have been treated seperately from several sources.

## Dataset


Currently the dataset includes technical articles from the year 2017 and 2018, mainly from these source

* [The Verge](http://www.theverge.com)
* [The next web](http://www.thenextweb.com)
* [Venture beat](http://www.venturebeat.com)
* [Ars Technica](http://www.arstechnica.com)
* [Tech Republic](http://www.techrepublic.com)
* [Engadget](http://www.engadget.com)
* [Zdnet](http://www.zdnet.com)

The database contains around 200.000 articles and is growing by the week. It is updated every week with the latest tech news.

## Currently deployed

### Web application

The web application is currently accessible [here](http://www.techcontroversy.com).

### Similar articles and conteroversial topics

You can find "controversial" topics in the database. [You can browse through the articles](http://www.techcontroversy.com/duplicates) that have been paired because the system considers it likely that they are talking about the same topic, possibly under a different slant.

Articles about the same stories can be found on the first page [aggregated here](http://www.techcontroversy.com/show_groups).

### Finding Related articles


[You can copy the text of a technical article into this text page](http://www.techcontroversy.com/search)  and find similar articles in the dataset, possibly limiting the search in a date interval.

Alternatively, you can see how articles in the database related to each other [entering the url of an article in this page](http://www.techcontroversy.com/search_url).

## Browser plugin

Alternatively you can use browser plugins for [Chrome](https://chrome.google.com/webstore/detail/tech-controversy-companio/mpiecgnniielnaiapcopieglhiemadhg) or [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tech-controversy-companion/)

### Description

This plugin adds a button on your toolbar. When you find an article on a tech news portal, click on the extension's icon on the toolbar to open a tab showing a list of articles related to the same story, gathered from other tech news portals on the site http://techcontroversy.com. 
If the article cannot be found in Techcontroversy's database, it will be submitted for processing by the nightly batch - come on the next day to get results.
The following tech news portals are supported:
Arstechnica, Thenextweb, Theverge, Venturebeat, Techrepublic, Wired, Engadget, Gizmodo, Mashable, Zdnet, Digitaltrends, Theguardian,
Qz, Inquisitr, Recode, Reuters, Techdirt, Inverse, Bleepingcomputer, Inc, Cnbc, Cnet, Forbes, Digit, Techtimes.

## Video introduction

A video introduction to this project can be found on my [Youtube channel](https://www.youtube.com/channel/UCHf5Uk_0nawvJDx3oA7WziA/).
