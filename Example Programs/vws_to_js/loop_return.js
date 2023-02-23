let x = function () {
    for (let i = 1; false; i++) {
        if ((i+1)**2 - i**2 > 100) {
            return i;
        }
    }
}();
console.log(`The smallest n so that (n+1)^2 - n^2 > 100: ${x}`);