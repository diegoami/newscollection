


find_similar = function(url) {
    var mainForm = document.getElementById("mainForm");
    mainForm.action = '/retrieve_similar_url';
    document.getElementById("tdidf_input").value = url;

    mainForm.target= "_blank";
    mainForm.submit();

}

select_header = function(element) {

    var topNav_element = document.getElementById(element);
    topNav_element.setAttribute("class", "active");
}

submit_story = function(method, id1, id2) {
    var mainForm = document.getElementById("samestory");
    mainForm.action = '/'+method+'/'+id1+'/'+id2;
    main.form.submit();
}