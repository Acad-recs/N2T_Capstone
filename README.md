# Nand to Tetris — Capstone Project
**Student:** Anveshna  
**Roll Number:** 2501010130  
**Personal Parameter ($K$):** 30 ($K \bmod 3 = 0$, $K \bmod 4 = 2$)

---

## Overview

This repository contains the complete implementation of the Nand to Tetris Capstone Project, bridging hardware architecture, systems programming, and low-level software design:

1. **Part A — Hack Computer Architecture (HDL)**: Complete implementation of `CPU.hdl`, `Memory.hdl`, and `Computer.hdl` verified using the official Nand to Tetris Hardware Simulator.
2. **Part B — Hack Two-Pass Assembler (Python)**: Robust assembler (`assembler.py`) translating Hack assembly (`.asm`) into binary machine code (`.hack`) matching the official Nand to Tetris Assembler. Implements personalized feature $K \bmod 3 = 0$: `symbols.txt` generation containing resolved label and variable memory addresses.
3. **Part C — Interactive Keyboard Rectangle Program (Hack Assembly)**: `Box.asm` rendered at starting row $K = 30$, height $20$ rows, and width $48$ pixels ($3$ 16-bit words) positioned at the left edge. Continuously monitors keyboard input to draw and clear the box in real time.

---

## Directory Structure

```text
N2T_Capstone/
├── README.md
├── LICENSE
├── .gitignore
└── capstone/
    ├── README.md
    ├── part-a-computer/
    │   ├── CPU.hdl
    │   ├── Memory.hdl
    │   ├── Computer.hdl
    │   ├── tests/
    │   └── results/
    ├── part-b-assembler/
    │   ├── assembler.py
    │   ├── tests/
    │   ├── test_programs/
    │   └── output/
    ├── part-c-box/
    │   ├── Box.asm
    │   └── Box.hack
    ├── screenshots/
    ├── docs/
    │   ├── architecture.md
    │   ├── assembler-design.md
    │   ├── box-program.md
    │   └── viva-preparation.md
    └── report/
```

For complete technical specifications and run instructions, see [capstone/README.md](file:///c:/Users/WINNTUSIT/Desktop/N2T_Capstone/capstone/README.md).
