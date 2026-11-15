// Nand to Tetris - Capstone Project - Part C
// File name: Box.asm
//
// Author: Anveshna (Roll No. 2501010130)
// Personal Parameter: K = 30
// Dimensions:
// - Starting row: K = 30
// - Height: 20 rows (rows 30 through 49)
// - Width: 16 * ((30 mod 4) + 1) = 16 * (2 + 1) = 48 pixels (3 words per row)
// - Position: Left edge of screen (words 0, 1, 2 of each row)
//
// Behaviour:
// - Continuously monitors keyboard memory register (KBD, address 24576).
// - When any key is pressed (RAM[KBD] != 0):
//     Fills the rectangle with solid black (-1, 0xFFFF).
// - When no key is pressed (RAM[KBD] == 0):
//     Clears the rectangle to white (0, 0x0000).
//
// Screen memory layout:
// - Screen base address: SCREEN = 16384
// - Each screen row = 32 words = 512 pixels
// - Row 30 starting address: SCREEN + 32 * 30 = 16384 + 960 = 17344

(LISTEN)
    // Read current state of keyboard
    @KBD
    D=M

    // If D != 0 (key pressed), color is black (-1)
    // If D == 0 (no key), color is white (0)
    @DRAW_BLACK
    D;JNE

    // Default to white (color = 0)
    @color
    M=0
    @RENDER
    0;JMP

(DRAW_BLACK)
    // Set color to black (-1)
    @color
    M=-1

(RENDER)
    // Initialize row counter: row = 20
    @20
    D=A
    @row
    M=D

    // Base address of starting row: SCREEN + 960 = 17344
    @17344
    D=A
    @addr
    M=D

(ROW_LOOP)
    // If row == 0, finished rendering all 20 rows -> return to LISTEN
    @row
    D=M
    @LISTEN
    D;JEQ

    // Read color into D
    @color
    D=M

    // Word 0 (pixels 0..15): RAM[addr] = color
    @addr
    A=M
    M=D

    // Word 1 (pixels 16..31): RAM[addr + 1] = color
    @addr
    A=M+1
    M=D

    // Word 2 (pixels 32..47): RAM[addr + 2] = color
    @addr
    A=M+1
    A=A+1
    M=D

    // Advance address to next row: addr = addr + 32
    @32
    D=A
    @addr
    M=D+M

    // Decrement row counter: row = row - 1
    @row
    M=M-1

    @ROW_LOOP
    0;JMP
