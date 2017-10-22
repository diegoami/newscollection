find_similar = function(url) {
    var mainForm = document.getElementById("mainForm");
    mainForm.action = '/retrieve_similar_url';
    document.getElementById("tdidf_input").value = url;
    alert( document.getElementById("tdidf_input").value );
    mainForm.target= "_blank";
    mainForm.submit();

}