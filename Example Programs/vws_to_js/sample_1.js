PI = 3.14156;
let n = 12395n;
let x = 129.23e023;
let h = .2;

z = function () {
    if (x > n) {
        return function () {
            document.getElementById('ID2').innerHTML = 'Hey There';
        };
    } else {
        return function () {
            document.getElementById('ID' + x).innerHTML = 'What\'s the time?';
        };
    }
}();

x = /^h(a|e)llo$/g;
const l = 'Hello';