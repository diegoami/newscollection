function submit_tfidf() {
    var selectionText = document.getElementById('tdidf_input').value
    var data = {text : selectionText , n_articles : 15}

    execute_tfidf(data);
}


function submit_doc2vec() {
    var selectionText = document.getElementById('doc2vec_input').value
    var data = {text : selectionText , n_articles : 15}

    execute_doc2vec(data);
}