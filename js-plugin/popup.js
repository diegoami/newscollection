
chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 15}

    execute_tfidf(data);
    execute_doc2vec(data);

});