# Nand to Tetris Capstone Project — Academic Report

**Course:** Nand to Tetris Capstone Project  
**Author / Student Name:** Anveshna  
**University Roll Number:** 2501010130  
**Submission Platform:** ZOSIMA Academic Portal  
**Date:** November 13, 2026  

---

## 1. Student Identification & Parameters

According to the capstone specification, the personalized parameters are derived from the student's university roll number:
- **University Roll Number:** `2501010130`
- **Personal Number ($K$):** Last two digits of roll number = **30**
- **Personalized Assembler Feature ($K \bmod 3$):**  
  $$30 \bmod 3 = 0$$  
  **Required Feature:** Generate `symbols.txt` containing all labels, variables, and predefined symbols with their resolved memory addresses (decimal and hexadecimal).
- **Personalized Rectangle Dimensions ($K \bmod 4$):**  
  $$30 \bmod 4 = 2$$  
  - **Starting Row:** $K = 30$  
  - **Height:** 20 screen rows (rows 30 to 49 inclusive)  
  - **Width:** $16 \times ((30 \bmod 4) + 1) = 16 \times 3 = 48\text{ pixels}$ (3 consecutive 16-bit words per row)  
  - **Horizontal Position:** Left edge of display (words 0, 1, and 2)  
  - **Color:** Solid black (`-1` / `0xFFFF`) when any key is pressed; solid white (`0` / `0x0000`) when key is released.  

---

## 2. Project Architecture & Components Summary

### Part A — Hack Computer Architecture (HDL)
The Hack Computer is a 16-bit Von Neumann architecture machine implementing a unified address space for data RAM, screen memory-mapped I/O, and keyboard memory-mapped input:
1. **`CPU.hdl`**: Integrates an Arithmetic Logic Unit (ALU), an Address Register (A), a Data Register (D), and a Program Counter (PC). Fully decodes Hack A-instructions (`@value`) and C-instructions (`dest=comp;jump`), manages memory write enable (`writeM`), memory addressing (`addressM`), and evaluates jump conditions based on ALU status flags (`zr`, `ng`).
2. **`Memory.hdl`**: Implements the full 32K memory space using high address bits `address[13..14]` to partition:
   - `0x0000`–`0x3FFF` (0 to 16,383): RAM16K
   - `0x4000`–`0x5FFF` (16,384 to 24,575): Screen (8K memory map)
   - `0x6000` (24,576): Keyboard memory register
3. **`Computer.hdl`**: Coordinates ROM32K, CPU, and Memory with reset synchronization.

### Part B — Two-Pass Hack Assembler (Python)
A fully modular assembler (`assembler.py`) developed in Python:
- **Lexical cleaning:** Strips inline comments (`//...`), whitespace, and ignores blank lines while preserving line indices for diagnostics.
- **Pass 1 (Symbol Resolution):** Scans the assembly stream, identifies label declarations `(LABEL)`, and records their target ROM instruction addresses in the symbol table without advancing the program counter.
- **Pass 2 (Binary Generation):** Translates A-instructions (`@value` or `@symbol`) and C-instructions (`dest=comp;jump`). Allocates new variable symbols dynamically to RAM addresses starting at `RAM[16]`.
- **Personalized Feature:** Automatically exports `symbols.txt` containing resolved label and variable mappings.
- **Verification:** Successfully assembled `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm` (27,483 instructions), verifying exact 100% bit-for-bit equivalence against the official course assembler.

### Part C — Keyboard-Controlled Box Program (Hack Assembly)
Written in Hack Assembly (`Box.asm`) and compiled exclusively with our custom `assembler.py`:
- Continuously polls keyboard memory register `RAM[24576]` (`KBD`).
- If `RAM[KBD] != 0`, sets fill color to `-1` (black); if `RAM[KBD] == 0`, sets fill color to `0` (white).
- Calculates the base address of Row 30:
  $$\text{Address} = \text{SCREEN} + (32 \times 30) = 16384 + 960 = 17344$$
- Iterates through 20 rows, writing the active color to 3 consecutive words (`addr`, `addr+1`, `addr+2`), advancing 32 words per row.

---

## 3. Test Verification & Empirical Results

### Hardware Simulator Test Suite (Part A)
All 5 mandatory test scripts were executed using the official Nand to Tetris Hardware Simulator:
- `CPU.tst` $\implies$ **End of script - Comparison ended successfully**
- `Memory.tst` $\implies$ **End of script - Comparison ended successfully**
- `ComputerAdd.tst` $\implies$ **End of script - Comparison ended successfully**
- `ComputerMax.tst` $\implies$ **End of script - Comparison ended successfully**
- `ComputerRect.tst` $\implies$ **End of script - Comparison ended successfully**

### Assembler Verification Results (Part B)
| Program | Number of Instructions | Custom Assembler Output | Official Assembler Output | Match Status |
|---|---|---|---|---|
| `Add.asm` | 6 | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/output/Add.hack` | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/test_programs/Add.hack` | **Exact Bit-for-Bit Match** |
| `Max.asm` | 16 | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/output/Max.hack` | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/test_programs/Max.hack` | **Exact Bit-for-Bit Match** |
| `Rect.asm` | 25 | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/output/Rect.hack` | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/test_programs/Rect.hack` | **Exact Bit-for-Bit Match** |
| `Pong.asm` | 27,483 | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/output/Pong.hack` | `NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/test_programs/Pong.hack` | **Exact Bit-for-Bit Match** |

### CPU Emulator Box Program Verification (Part C)
Testing via the CPU Emulator demonstrated strict boundary compliance:
```text
|RAM[24576]|RAM[17312]|RAM[17344]|RAM[17345]|RAM[17346]|RAM[17347]|RAM[17952]|RAM[17953]|RAM[17954]|RAM[17984]|
|        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |  (Key Released)
|       65 |        0 |       -1 |       -1 |       -1 |        0 |       -1 |       -1 |       -1 |        0 |  (Key Pressed)
|        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |  (Key Released)
```
- **Row boundaries:** Above row (RAM[17312]) and below row (RAM[17984]) remained 0.
- **Column boundaries:** Column word 3 (RAM[17347]) remained 0.
- **Screen artifacts:** Visual screen output confirmed solid black box of 48 pixels by 20 rows during keypress, fully clearing upon release.

---

## 4. Engineering Reflection: A Genuine Mistake Encountered and Fixed

During the implementation of Part C (`Box.asm`), an initial calculation error occurred when advancing the screen row memory pointer. The Hack ALU instruction set does not support arbitrary register additions like `M=M+D` as a symmetric primitive; instead, the Hack hardware only defines the ALU computation `D+M` where `D` serves as the first operand (`x`) and `M` serves as the second operand (`y`). Attempting to assemble `@addr; M=M+D` initially failed during compilation with our custom assembler reporting an invalid computation expression. Furthermore, when determining row offset increments, an initial test used a hardcoded single-word offset that failed to jump across the full 32-word stride of a screen scanline. This was corrected by properly loading the constant 32 into the D register (`@32; D=A`) and performing `@addr; M=D+M`, correctly maintaining scanline alignment across all 20 rows.

---

## 5. Conclusion

All three components of the Nand to Tetris Capstone Project have been implemented from first principles, verified against official course tools, and documented to academic standards. The repository contains full source code, machine-readable verification logs, visual output artifacts, and git history demonstrating genuine engineering progression.
