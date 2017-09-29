chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 10}
    var xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://127.0.0.1:5000/gensim/', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'http://127.0.0.1:5000/doc2vec/', true);
    xhr2.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function() {//Call a function when the state changes.

        response_text = JSON.parse(xhr.responseText)

        related_articles = response_text["related_articles"]
        text = ""
        for (i = 0; i < related_articles.length; i++) {
            ctext=""
            article = related_articles[i]
            tags = article['tags']
            tag_base = article['tag_base']
            ctext +='<B class="sourceLink">('
            ctext += article['source']
            ctext += ')</B>&nbsp;&nbsp;'
            ctext += '<A class="articleLink" HREF="'
            ctext +=  article['url']
            ctext +=   '">'+article['title']+'</A>'
            ctext += '(' + Number(article['similarity'].toFixed(2)) + '%)'
            ctext +=      '<br>'
            if (tags.length > 0)
                ctext += 'Tags: '
            for (j = 0; j < tags.length; j++) {
                tagx = tags[j]
                tagb = tag_base[j]
                ctext +=      '<A HREF="'
                ctext +=    tagx
                ctext +=   '">'+tagb+'</A>'
                if (j+1 < tags.length )
                    ctext += ',&nbsp;'
            }
            ctext +=     '<br>';

            text += ctext
            text += '<br>';

        }

        document.getElementById("output").innerHTML = text;
     }

     xhr2.onreadystatechange = function() {//Call a function when the state changes.

        response_text = JSON.parse(xhr2.responseText)

        related_articles = response_text["related_articles"]
        text = ""
        for (i = 0; i < related_articles.length; i++) {
            ctext=""
            article = related_articles[i]
            tags = article['tags']
            tag_base = article['tag_base']
            ctext +='<B class="sourceLink">('
            ctext += article['source']
            ctext += ')</B>&nbsp;&nbsp;'
            ctext += '<A class="articleLink" HREF="'
            ctext +=  article['url']
            ctext +=   '">'+article['title']+'</A>'
            ctext += '(' + Number(article['similarity'].toFixed(2)) + '%)'
            ctext +=      '<br>'
            if (tags.length > 0)
                ctext += 'Tags: '
            for (j = 0; j < tags.length; j++) {
                tagx = tags[j]
                tagb = tag_base[j]
                ctext +=      '<A HREF="'
                ctext +=    tagx
                ctext +=   '">'+tagb+'</A>'
                if (j+1 < tags.length )
                    ctext += ',&nbsp;'
            }
            ctext +=     '<br>';

            text += ctext
            text += '<br>';

        }

        document.getElementById("output2").innerHTML = text;
    }

    xhr.send(JSON.stringify(data));

    xhr2.send(JSON.stringify(data));



});