load Box.hack,
// Initial state: no key pressed, run 500 cycles
set RAM[24576] 0,
repeat 500 {
    ticktock;
}

// Press key (e.g. key code 65 'A')
set RAM[24576] 65,
repeat 2000 {
    ticktock;
}

// Check screen addresses: row 30 is 16384 + 32 * 30 = 17344
// First row words: 17344, 17345, 17346 should be -1
// Row 49 words: 16384 + 32 * 49 = 17952, 17953, 17954 should be -1
// Outside rectangle: row 29 (17312) should be 0, row 50 (17984) should be 0, word 3 (17347) should be 0

// Release key
set RAM[24576] 0,
repeat 2000 {
    ticktock;
}
