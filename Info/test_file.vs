a = [1, 2, 100, -2, 5, 0.5];

for i in a step 2 {
    log(a);
}

log(...a.map(#x: x*4));

// Output:
// 1
// 100
// 5
// 4 8 400 -8 20 2