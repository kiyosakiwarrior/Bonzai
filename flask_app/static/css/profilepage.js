

function changeName() {
    document.querySelector(".h3special").innerText = "Thanos";
}

var el1 = document.getElementById('friendrequest1');
var el2 = document.getElementById('friendrequest2');
var requests = 2
var connections = 500

function friendnotification1() {
    el1.remove();
    requests--
    document.querySelector(".circle").innerText= requests
}
function friendnotification1plus() {
    el1.remove();
    requests--
    document.querySelector(".circle").innerText = requests
    connections++
    document.querySelector(".circle2").innerText = connections
}
function friendnotification2() {
    el2.remove();
    requests--
    document.querySelector(".circle").innerText = requests
}
function friendnotification2plus() {
    el2.remove();
    requests--
    document.querySelector(".circle").innerText = requests
    connections++
    document.querySelector(".circle2").innerText = connections
}