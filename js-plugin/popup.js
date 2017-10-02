function create_inner_text(response_text) {
    var related_articles = response_text["related_articles"]
    var text = ""
    for (i = 0; i < related_articles.length; i++) {
        var ctext = ""
        var article = related_articles[i]
        var tags = article['tags']
        var tag_base = article['tag_base']
        var authors = article['authors']
        var author_base = article['author_base']
        ctext += '<A class="articleLink" HREF="'
        ctext += article['url']
        ctext += '">' + article['title'] + '</A>'
        ctext += '<br>'

        ctext += '<B class="sourceLink">('
        ctext += article['source']
        ctext += ')</B>&nbsp;&nbsp;'
        ctext += '<I>'+article['date']+'</I>'

        ctext += '&nbsp;&nbsp;'
        ctext += '(' + Number(article['similarity'].toFixed(2)) + '%)'
        ctext += '&nbsp;&nbsp;'
        ctext += '<br>'
        if (tags.length > 0)
            ctext += 'Tags: '
        for (j = 0; j < tags.length; j++) {
            var tagx = tags[j]
            var tagb = tag_base[j]
            ctext += '<A HREF="'
            ctext += tagx
            ctext += '">' + tagb + '</A>'
            if (j + 1 < tags.length)
                ctext += ',&nbsp;'
        }
        if (authors.length > 0)
            ctext += '&nbsp;&nbsp;Authors: '
        for (j = 0; j < authors.length; j++) {
            var autorx = authors[j]
            var autorb = author_base[j]
            ctext += '<A HREF="'
            ctext += autorx
            ctext += '">' + autorb+ '</A>'
            if (j + 1 < authors.length)
                ctext += ',&nbsp;'
        }
        ctext += '<br>';

        text += ctext
        text += '<br>';
    }
    return text
}

function execute_tfidf(data) {
    var xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://127.0.0.1:5000/gensim/', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function () {
        var response_text = JSON.parse(xhr.responseText)
        var text = create_inner_text(response_text);
        document.getElementById("output").innerHTML = text;
    }

    xhr.send(JSON.stringify(data));
}

function execute_doc2vec(data) {
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'http://127.0.0.1:5000/doc2vec/', true);
    xhr2.setRequestHeader('Content-type', 'application/json');

    xhr2.onreadystatechange = function () {
        var response_text = JSON.parse(xhr2.responseText)
        var text = create_inner_text(response_text);
        document.getElementById("output2").innerHTML = text;
    }

    xhr2.send(JSON.stringify(data));
}

chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 15}

    execute_tfidf(data);
    execute_doc2vec(data);

});