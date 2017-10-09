
chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 15}
    if (data.text) {
        var remote_h = get_remote_hostname_port()

        execute_tfidf(data, remote_h.hostname, remote_h.port);
        execute_doc2vec(data, remote_h.hostname, remote_h.port);
    } else {
        alert("Please select the full text of a technical article")
    }

});