# Nand to Tetris Capstone — Viva Voce Preparation Guide

**Student:** Anveshna  
**Roll Number:** 2501010130  
**Personal Parameter ($K$):** 30  
**Presentation Time:** 5 Minutes  

---

## 1. Five-Minute Pitch Structure

### Minute 1: Project Scope & Architecture (Part A)
- *"Good morning/afternoon. In this capstone project, I constructed the complete vertical stack of the Hack computing platform: the hardware architecture in HDL, the systems assembler in Python, and an interactive keyboard-driven graphical program in Hack assembly."*
- *"In Part A, I implemented the Hack CPU, Memory subsystem, and Computer chip. The CPU integrates an ALU, A-register, D-register, and Program Counter. The instruction set differentiates between 15-bit address constants (A-instructions) and 16-bit microcoded ALU/destination/jump commands (C-instructions). Memory maps 16K of data RAM, 8K of screen buffer, and 1 keyboard register across a 32K address space using address bits 13 and 14."*

### Minute 2: Systems Software & Two-Pass Assembler (Part B)
- *"In Part B, I built a two-pass assembler in Python. The first pass builds the symbol table by scanning for `(LABEL)` pseudocodes and recording their ROM instruction addresses without incrementing the program counter."*
- *"The second pass translates A-instructions and C-instructions into 16-bit binary machine words. Any newly encountered variable is dynamically assigned to RAM starting at address 16. My personal number $K = 30$ ($K \bmod 3 = 0$) requires the export of all resolved symbols to `symbols.txt`. I validated my assembler against the official course assembler on `Add`, `Max`, `Rect`, and `Pong` (over 27,000 instructions) achieving a 100% bit-for-bit match."*

### Minute 3: Low-Level Graphics & Interactive Assembly (Part C)
- *"In Part C, I authored `Box.asm` to draw a keyboard-controlled rectangle. With $K=30$, the program starts at row 30, spans 20 rows in height, and has a width of 48 pixels ($16 \times ((30 \bmod 4) + 1)$), which translates to exactly 3 memory words per row."*
- *"The program polls `KBD` (RAM[24576]). When a key is detected, it fills words 0, 1, and 2 with `-1` (black) across rows 30 to 49, starting at screen address $16384 + (32 \times 30) = 17344$. When released, it overwrites the exact region with `0` (white). I compiled it using my own assembler and verified it in the CPU Emulator."*

### Minute 4–5: Demonstration & Live Modifications
- Demonstrate test script executions or live CPU Emulator screen output.
- Walk through live code modifications requested by examiners.

---

## 2. Anticipated Technical Questions & Answers

### Q1: How does the CPU distinguish between A-instructions and C-instructions?
**Answer:** The most significant bit (`instruction[15]`) acts as the opcode.
- If `instruction[15] == 0`, it is an A-instruction. Bits `[0..14]` represent a 15-bit constant loaded into the A-register.
- If `instruction[15] == 1`, it is a C-instruction. Bits `[13..14]` are unused (`11`), bit 12 selects between A or M as the ALU input, bits `[6..11]` drive the ALU control lines (`zx, nx, zy, ny, f, no`), bits `[3..5]` drive the destination registers (`A, D, M`), and bits `[0..2]` govern conditional jumps.

### Q2: Why does the Hack assembler require two passes?
**Answer:** Because of forward referencing. A program may jump to a label before that label is declared in the code (e.g., `@LOOP; 0;JMP` followed later by `(LOOP)`). The first pass discovers and records all label addresses into a symbol table so that during the second pass, all targets are known and can be encoded into binary A-instructions immediately.

### Q3: How is screen memory addressed in Hack hardware?
**Answer:** The Hack screen has a resolution of $512 \times 256$ pixels. Each row consists of 512 pixels, which equals 32 16-bit words ($512 / 16 = 32$). The screen memory map begins at base address `SCREEN = 16384` (`0x4000`). To address row $r$ and column-word $c$, the formula is:
$$\text{Address} = 16384 + (32 \times r) + c$$

### Q4: How does keyboard input detection work without interrupts?
**Answer:** The Hack computer uses polling (memory-mapped I/O). The physical keyboard hardware continuously latches the ASCII code of whatever key is currently pressed into memory location `RAM[24576]` (`KBD`). When no key is pressed, this register holds 0. The program reads `RAM[KBD]` in an infinite loop (`(LISTEN)`) to detect changes in real time.

---

## 3. Rapid Live Code Modifications (Examiner Tests)

### Scenario A: Move the box down by 10 rows (from Row 30 to Row 40)
**Modification in `Box.asm`:**
Change the base address constant:
$$\text{New Address} = 16384 + (32 \times 40) = 16384 + 1280 = 17664$$
In `Box.asm`:
```hack
// Replace:
@17344
D=A
@addr
M=D

// With:
@17664
D=A
@addr
M=D
```

### Scenario B: Increase the height to 30 rows
**Modification in `Box.asm`:**
```hack
// Replace:
@20
D=A
@row
M=D

// With:
@30
D=A
@row
M=D
```

### Scenario C: Widen the rectangle from 3 words (48 pixels) to 4 words (64 pixels)
**Modification in `Box.asm`:**
Inside `(ROW_LOOP)`, add writing to the 4th word:
```hack
// Word 3 (pixels 48..63): RAM[addr + 3] = color
@addr
A=M+1
A=A+1
A=A+1
M=D
```
