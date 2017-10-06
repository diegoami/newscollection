
xhr2_waiting = 0
xhr_waiting = 0
hostname = window.location.hostname
//hostname = '127.0.0.1'
//hostname = 'ec2-35-156-126-138.eu-central-1.compute.amazonaws.com'


function submit_all() {
    var selectionText = document.getElementById('tdidf_input').value
    var n_articles_value = document.getElementById('n_articles').value
    var start = document.getElementById('start').value
    var end = document.getElementById('end').value

    var data = {text : selectionText , n_articles : n_articles_value, start: start, end: end}
    execute_tfidf(data);
    execute_doc2vec(data);

}


function check_enable_button() {
    if ((xhr_waiting == 0) && (xhr2_waiting == 0)) {
        document.getElementById("submit_interesting").value = "Submit"
        document.getElementById("submit_interesting").disabled = false
    }

}


function disable_button() {
    if ((xhr_waiting == 1) || (xhr2_waiting == 1)) {
        document.getElementById("submit_interesting").value = "Please wait...."
        document.getElementById("submit_interesting").disabled = true
    }
}


function submit_interesting() {
    var n_articles_value = document.getElementById('n_articles').value
    var start = document.getElementById('start').value
    var end = document.getElementById('end').value

    var data = { n_articles : n_articles_value, start: start, end: end}

    if (xhr2_waiting == 0) {
        xhr2_waiting = 1
        execute_doc2vec_interesting(data);
    }
    if (xhr_waiting == 0) {
        xhr_waiting = 1;
        execute_tfidf_interesting(data);
    }

    disable_button()
}

function create_short_text_for_article(article) {
    var ctext = ""
    ctext += '<A class="articleSmall" HREF="'
    ctext += article['url']
    ctext += '">' + article['title'] + '</A>'
    ctext += '<br>'

    ctext += '<B class="sourceSmall">('
    ctext += article['source']
    ctext += ')</B>&nbsp;&nbsp;'
    ctext += '<I>' + article['date'] + '</I>'


    ctext += '&nbsp;&nbsp;'
    ctext += '<br>'
    return ctext
}

function create_text_for_article(article) {
    var ctext = ""
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
    ctext += '<I>' + article['date'] + '</I>'

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
        ctext += '">' + autorb + '</A>'
        if (j + 1 < authors.length)
            ctext += ',&nbsp;'
    }
    ctext += '<br>';
    return ctext;
}

function create_inner_text(related_articles) {
    var text = ""
    for (i = 0; i < related_articles.length; i++) {

        var article = related_articles[i]
        var ctext = create_text_for_article(article);


        text += ctext
        text += '<br>';

        var connected_articles = article['connected_articles']
        if (connected_articles && connected_articles.length > 0) {
            text += '<I>Other sources</I><BR>';
            for (j = 0; j < connected_articles.length; j++) {
                var connected_article = connected_articles[j]
                var cctext = create_short_text_for_article(connected_article)
                text += cctext

            }
             text += '<br><br><br>'
        }

    }
    return text
}

function execute_tfidf(data) {
    var xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://'+hostname+':8080/tfidf/v1/related/', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function () {
        var response_text = JSON.parse(xhr.responseText)
        var related_articles = response_text["related_articles"]
        var text = create_inner_text(related_articles);
        document.getElementById("output").innerHTML = text;
    }

    xhr.send(JSON.stringify(data));
}

function execute_doc2vec(data) {
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'http://'+hostname+':8080/doc2vec/v1/related/', true);
    xhr2.setRequestHeader('Content-type', 'application/json');

    xhr2.onreadystatechange = function () {
        var response_text = JSON.parse(xhr2.responseText)
        var related_articles = response_text["related_articles"]
        var text = create_inner_text(related_articles);
        document.getElementById("output2").innerHTML = text;
    }

    xhr2.send(JSON.stringify(data));
}


function execute_tfidf_interesting(data) {
    var xhr = new XMLHttpRequest();

    xhr.open('POST', 'http://'+hostname+':8080/tfidf/v1/interesting/', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onreadystatechange = function () {
        var response_text = JSON.parse(xhr.responseText)
        var interesting_articles = response_text["interesting_articles"]
        var text = create_inner_text(interesting_articles);
        document.getElementById("output").innerHTML = text;
        xhr_waiting = 0
        check_enable_button()

    }

    xhr.send(JSON.stringify(data));
}

function execute_doc2vec_interesting(data) {
    var xhr2 = new XMLHttpRequest();
    xhr2.open('POST', 'http://'+hostname+':8080/doc2vec/v1/interesting/', true);
    xhr2.setRequestHeader('Content-type', 'application/json');

    xhr2.onreadystatechange = function () {
        var response_text = JSON.parse(xhr2.responseText)
        var interesting_articles = response_text["interesting_articles"]
        var text = create_inner_text(interesting_articles);
        document.getElementById("output2").innerHTML = text;
        xhr2_waiting = 0
        check_enable_button()

    }

    xhr2.send(JSON.stringify(data));
}
