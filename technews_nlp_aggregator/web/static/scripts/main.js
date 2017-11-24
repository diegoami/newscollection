


find_similar = function(article_id) {
    var mainForm = document.getElementById("mainForm");
    mainForm.action = '/retrieve_similar_url';
    document.getElementById("article_id").value = article_id;
    document.getElementById("search_url").value = '';
    mainForm.target= "_blank";
    mainForm.submit();
}

select_header = function(element) {
    $(".nav li").removeClass("active");//this will remove the active class from
                                     //previously active menu item
    $(element).addClass('active');
}



submit_story = function(method, id1, id2) {
    document.getElementById("yes_button").disabled = true;
    document.getElementById("almost_button").disabled = true;
    document.getElementById("no_button").disabled = true;


    var mainForm = document.getElementById("samestory");
    mainForm.action = '/'+method+'/'+id1+'/'+id2;
    mainForm.submit();
}

random_url = function() {
    var mainForm = document.getElementById("mainForm");
    mainForm.action = '/random_url';
    mainForm.submit();
}

random_article_id = function() {
    var statisticsForm = document.getElementById("statistics_form");
    statisticsForm.action = '/statistics_random';
    statisticsForm.submit();
}

skip = function() {
    window.location.href = '/random_related';

}


function send_same_story(method, id1, id2, element_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/'+method+'/'+id1+'/'+id2, true);

    xhr.onreadystatechange = function () {
        var response_text = xhr.responseText ;
        document.getElementById(element_id).innerHTML = response_text ;
    }
    xhr.send();
}

function request_summary(id, element_id, text_id, title_element_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/summary/'+id,   true);
    document.getElementById(element_id).innerHTML = 'Processing....'
    xhr.onreadystatechange = function () {
        var response_text = xhr.responseText ;
        document.getElementById(element_id).innerHTML = '<P class="article_text"><B>'+ document.getElementById(title_element_id).innerHTML+'.</B> </P><P></P>'
        document.getElementById(text_id).innerHTML = response_text ;
    }
    xhr.send();
}

function move_to_page(page_id) {
    var mainForm = document.getElementById("mainForm");
    document.getElementById("page_id").value = page_id
    mainForm.target= "";
    mainForm.submit();
}

