# Nand to Tetris — Capstone Project & Course Submission

**Student:** Anveshna  
**Roll Number:** 2501010130  
**Personal Parameter ($K$):** 30 ($K \bmod 3 = 0$, $K \bmod 4 = 2$)

---

## 🏛️ Official University Submission Structure

This repository is structured according to the official university submission requirements:

```text
N2T_Capstone/
├── README.md
├── LICENSE
├── .gitignore
└── NAND to Tetris_Anveshna_2501010130/
    ├── 1. Theory Assignments/
    │   └── README.md                       # Assignment PDFs folder
    ├── 2. Lab Assignments/
    │   └── README.md                       # Lab assignment PDFs folder
    └── 3. Capstone Project/
        ├── academic_report.md              # Formal Academic Submission Report (ZOSIMA)
        └── Project Files/
            ├── README.md                   # Capstone Technical README
            ├── part-a-computer/            # Part A: HDL Computer Architecture
            │   ├── CPU.hdl
            │   ├── Memory.hdl
            │   ├── Computer.hdl
            │   ├── tests/                  # Official test scripts (.tst, .cmp)
            │   └── results/                # Actual simulation outputs (.out)
            ├── part-b-assembler/           # Part B: Two-Pass Python Assembler
            │   ├── assembler.py
            │   ├── tests/                  # Unit test suite
            │   ├── test_programs/          # Official benchmark assembly files (.asm)
            │   └── output/                 # Generated .hack binaries and symbols.txt
            ├── part-c-box/                 # Part C: Keyboard-Controlled Box Program
            │   ├── Box.asm
            │   ├── Box.hack
            │   ├── Box.out
            │   ├── BoxTest.tst
            │   └── symbols.txt
            ├── screenshots/                # CPU Emulator screen captures
            │   ├── box_screen_cleared.png
            │   └── box_screen_pressed.png
            └── docs/                       # Comprehensive Technical Documentation
                ├── architecture.md
                ├── assembler-design.md
                ├── attribution.md
                ├── box-program.md
                └── viva-preparation.md
```

---

## 🚀 Navigation & Quick Links

- **Formal Academic Report:** [`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/academic_report.md`](file:///c:/Users/WINNTUSIT/Desktop/N2T_Capstone/NAND%20to%20Tetris_Anveshna_2501010130/3.%20Capstone%20Project/academic_report.md)
- **Capstone Project Files:** [`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/`](file:///c:/Users/WINNTUSIT/Desktop/N2T_Capstone/NAND%20to%20Tetris_Anveshna_2501010130/3.%20Capstone%20Project/Project%20Files/)
- **Viva Voce Preparation Guide:** [`NAND to Tetris_Anveshna_2501010130/3. Capstone Project/Project Files/docs/viva-preparation.md`](file:///c:/Users/WINNTUSIT/Desktop/N2T_Capstone/NAND%20to%20Tetris_Anveshna_2501010130/3.%20Capstone%20Project/Project%20Files/docs/viva-preparation.md)

---

## 📋 Project Summary

1. **Part A — Hack Computer Architecture (HDL)**: Complete implementation of `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`. Verified and passed against all 5 official test scripts (`CPU.tst`, `Memory.tst`, `ComputerAdd.tst`, `ComputerMax.tst`, `ComputerRect.tst`) with exact comparison matching.
2. **Part B — Hack Two-Pass Assembler (Python)**: Robust assembler (`assembler.py`) translating Hack assembly (`.asm`) into binary machine code (`.hack`) matching the official Nand to Tetris Assembler bit-for-bit across `Add.asm`, `Max.asm`, `Rect.asm`, and `Pong.asm`. Implements personalized feature $K \bmod 3 = 0$: `symbols.txt` address resolution export.
3. **Part C — Interactive Keyboard Rectangle Program (Hack Assembly)**: `Box.asm` rendered at starting row $K = 30$, height $20$ rows, and width $48$ pixels ($3$ 16-bit words) positioned at the left edge. Continuously monitors keyboard input to draw and clear the box in real time.
