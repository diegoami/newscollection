
chrome.tabs.query({currentWindow: true, active: true}, function (tabs) {
    var mainForm = document.getElementById("url_input");
    document.getElementById("search_url").value = tabs[0].url;

    mainForm.submit();
});
