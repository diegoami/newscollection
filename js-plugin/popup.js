chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 10}
    var xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://127.0.0.1:5000/gensim/', true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() {//Call a function when the state changes.

        response_text = JSON.parse(xhr.responseText)

        related_articles = response_text["related_articles"]
        text = ""
        for (i = 0; i < related_articles.length; i++) {
            article = related_articles[i]
            tags = article['tags']
            ctext = ''
            ctext += '<A class="articleLink" HREF="'
            ctext +=  article['url']
            ctext +=   '">'+article['title']+'</A>'
            ctext += '(' + Number(article['similarity'].toFixed(2)) + '%)'
            ctext +=      '<br>'

                '<br>';

            text += ctext

        }

        document.getElementById("output").innerHTML = text;
    }

    xhr.send(JSON.stringify(data));

});