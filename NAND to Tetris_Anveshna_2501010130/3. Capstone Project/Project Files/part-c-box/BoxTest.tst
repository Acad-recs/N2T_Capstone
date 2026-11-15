load Box.hack,
output-file Box.out,
output-list RAM[24576]%D1.5.1 RAM[17312]%D1.6.1 RAM[17344]%D1.6.1 RAM[17345]%D1.6.1 RAM[17346]%D1.6.1 RAM[17347]%D1.6.1 RAM[17952]%D1.6.1 RAM[17953]%D1.6.1 RAM[17954]%D1.6.1 RAM[17984]%D1.6.1;

// 1. Initial idle (key = 0)
set RAM[24576] 0,
repeat 300 {
    ticktock;
}
output;

// 2. Key pressed (key = 65 'A') -> Rectangle drawn black (-1)
set RAM[24576] 65,
repeat 1500 {
    ticktock;
}
output;

// 3. Key released (key = 0) -> Rectangle cleared (0)
set RAM[24576] 0,
repeat 1500 {
    ticktock;
}
output;
