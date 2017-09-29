chrome.tabs.executeScript( {
    code: "window.getSelection().toString(); "
}, function(selection) {
    var data = {text : selection[0], n_articles : 10}

    function generate_links_text(response_text ) {
        related_articles = response_text["related_articles"]
        text = ""
        for (i = 0; i < related_articles.length; i++) {
            ctext = ""
            article = related_articles[i]
            tags = article['tags']
            tag_base = article['tag_base']
            ctext += '<B class="sourceLink">('
            ctext += article['source']
            ctext += ')</B>&nbsp;&nbsp;'
            ctext += '<A class="articleLink" HREF="'
            ctext += article['url']
            ctext += '">' + article['title'] + '</A>'
            ctext += '(' + Number(article['similarity'].toFixed(2)) + '%)'
            ctext += '<br>'
            if (tags.length > 0)
                ctext += 'Tags: '
            for (j = 0; j < tags.length; j++) {
                tagx = tags[j]
                tagb = tag_base[j]
                ctext += '<A HREF="'
                ctext += tagx
                ctext += '">' + tagb + '</A>'
                if (j + 1 < tags.length)
                    ctext += ',&nbsp;'
            }
            ctext += '<br>';

            text += ctext
            text += '<br>';

        }
    }

    var xhr = new XMLHttpRequest();


    xhr.open('POST', 'http://127.0.0.1:5000/gensim/', true);
    xhr.setRequestHeader('Content-type', 'application/json');
    xhr.onreadystatechange = function() {
        response_text = JSON.parse(xhr.responseText)


        text1 = generate_links_text(response_text);

        document.getElementById("output").innerHTML = text1;
    }

    xhr.send(JSON.stringify(data));

});