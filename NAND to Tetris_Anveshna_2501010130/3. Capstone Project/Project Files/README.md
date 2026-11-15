# Nand to Tetris Capstone Project Specification & Guide

**Author:** Anveshna  
**University Roll Number:** 2501010130  
**Personal Parameter ($K$):** $30$  
- $K \bmod 3 = 0 \implies$ Generate `symbols.txt` containing all labels and variables with their resolved addresses.
- $K \bmod 4 = 2 \implies$ Width = $16 \times ((2) + 1) = 48$ pixels ($3$ screen words per row).
- Starting row = $30$, Height = $20$ rows.

---

## Technical Components

### 1. Part A: Hack Computer Architecture (`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/`)
- `CPU.hdl`: Full central processing unit decoding A-instructions and C-instructions, steering ALU input, maintaining A-register, D-register, program counter (PC), and memory control flags (`writeM`, `addressM`, `outM`).
- `Memory.hdl`: Memory address space decoding (RAM16K: `0x0000-0x3FFF`, Screen: `0x4000-0x5FFF`, Keyboard: `0x6000`).
- `Computer.hdl`: Top-level integration of ROM32K, CPU, and Memory.
- **Official Tests**: `CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`.

### 2. Part B: Two-Pass Python Assembler (`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/`)
- `assembler.py`: CLI assembler supporting:
  - White space and comment stripping.
  - First-pass symbol resolution for ROM labels `(LABEL)`.
  - Second-pass instruction translation for A-instructions (`@value`, `@symbol`) and C-instructions (`dest=comp;jump`).
  - Predefined symbols (`R0`-`R15`, `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `SCREEN`, `KBD`) and dynamically allocated RAM variables starting at address 16.
  - Symbol table export to `symbols.txt` ($K \bmod 3 = 0$).

### 3. Part C: Keyboard-Controlled Box Program (`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-c-box/`)
- `Box.asm`: Assembly program polling memory location `KBD` (24576).
  - Key pressed $\neq 0 \implies$ draws solid black rectangle across rows 30 to 49 (width: 3 words / 48 pixels).
  - Key released ($= 0$) $\implies$ clears rectangle back to white.
- `Box.hack`: Compiled machine code output from `assembler.py`.

---

## Reproduction and Verification

### Running Hardware Simulator Tests
```powershell
# From repository root
./n2t_official/nand2tetris/tools/HardwareSimulator.bat NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/tests/CPU.tst
./n2t_official/nand2tetris/tools/HardwareSimulator.bat NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/tests/Memory.tst
./n2t_official/nand2tetris/tools/HardwareSimulator.bat NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/tests/ComputerAdd.tst
./n2t_official/nand2tetris/tools/HardwareSimulator.bat NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/tests/ComputerMax.tst
./n2t_official/nand2tetris/tools/HardwareSimulator.bat NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-a-computer/tests/ComputerRect.tst
```

### Running the Python Assembler
```powershell
python NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-b-assembler/assembler.py NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/part-c-box/Box.asm
```
