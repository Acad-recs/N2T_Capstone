#!/usr/bin/env python3
"""
Hack Computer Assembler (Nand to Tetris)
Translates Hack assembly language (.asm) programs into Hack machine code (.hack).

Author: Anveshna (Roll No. 2501010130)
Personalized Feature (K = 30, K % 3 = 0):
Generates 'symbols.txt' containing all labels and variables with their resolved addresses.
"""

import sys
import os
import re

# Predefined symbols defined in the Hack specification
PREDEFINED_SYMBOLS = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'SCREEN': 16384,
    'KBD': 24576,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,
    'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
    'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
}

# Computation bit patterns (a c1 c2 c3 c4 c5 c6)
COMP_TABLE = {
    # a = 0 (operations on A / D)
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    # a = 1 (operations on M / D)
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

# Destination bit patterns (d1 d2 d3)
DEST_TABLE = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'DM':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111',
    'ADM': '111'
}

# Jump bit patterns (j1 j2 j3)
JUMP_TABLE = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}


class HackAssembler:
    def __init__(self, k=30):
        self.k = k
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.variable_address = 16
        self.user_symbols = {}  # Tracks user-defined labels and variables

    def clean_line(self, line):
        """Removes comments and extraneous whitespace."""
        comment_idx = line.find('//')
        if comment_idx != -1:
            line = line[:comment_idx]
        return line.strip()

    def first_pass(self, lines):
        """
        First pass: Scan lines, strip comments and blanks,
        and assign ROM addresses to labels (LABEL).
        """
        rom_address = 0
        cleaned_instructions = []

        for line_num, raw_line in enumerate(lines, 1):
            line = self.clean_line(raw_line)
            if not line:
                continue

            # Check for label declaration (LABEL)
            if line.startswith('(') and line.endswith(')'):
                label = line[1:-1].strip()
                if not label:
                    raise ValueError(f"Line {line_num}: Empty label declaration '()'")
                if label not in self.symbol_table:
                    self.symbol_table[label] = rom_address
                    self.user_symbols[label] = rom_address
                else:
                    # Label already defined
                    pass
            else:
                cleaned_instructions.append((line_num, line))
                rom_address += 1

        return cleaned_instructions

    def translate_a_instruction(self, instruction, line_num):
        """Translates @value or @symbol into a 16-bit binary instruction."""
        symbol = instruction[1:].strip()
        if not symbol:
            raise ValueError(f"Line {line_num}: Invalid empty A-instruction '@'")

        if symbol.isdigit():
            address = int(symbol)
        else:
            if symbol not in self.symbol_table:
                # Allocate new variable in RAM starting at 16
                self.symbol_table[symbol] = self.variable_address
                self.user_symbols[symbol] = self.variable_address
                self.variable_address += 1
            address = self.symbol_table[symbol]

        if address < 0 or address > 32767:
            raise ValueError(f"Line {line_num}: Address {address} out of 15-bit range [0, 32767]")

        return f"0{address:015b}"

    def translate_c_instruction(self, instruction, line_num):
        """
        Translates dest=comp;jump into a 16-bit binary instruction.
        Format: 111 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3
        """
        dest_part = ""
        comp_part = ""
        jump_part = ""

        # Check for destination
        if '=' in instruction:
            dest_part, rest = instruction.split('=', 1)
            dest_part = dest_part.strip()
        else:
            rest = instruction

        # Check for jump
        if ';' in rest:
            comp_part, jump_part = rest.split(';', 1)
            comp_part = comp_part.strip()
            jump_part = jump_part.strip()
        else:
            comp_part = rest.strip()

        if comp_part not in COMP_TABLE:
            raise ValueError(f"Line {line_num}: Invalid computation expression '{comp_part}'")
        if dest_part not in DEST_TABLE:
            raise ValueError(f"Line {line_num}: Invalid destination expression '{dest_part}'")
        if jump_part not in JUMP_TABLE:
            raise ValueError(f"Line {line_num}: Invalid jump expression '{jump_part}'")

        comp_bits = COMP_TABLE[comp_part]
        dest_bits = DEST_TABLE[dest_part]
        jump_bits = JUMP_TABLE[jump_part]

        return f"111{comp_bits}{dest_bits}{jump_bits}"

    def second_pass(self, cleaned_instructions):
        """Second pass: translates instructions into 16-bit binary machine code."""
        machine_code = []
        for line_num, instruction in cleaned_instructions:
            if instruction.startswith('@'):
                code = self.translate_a_instruction(instruction, line_num)
            else:
                code = self.translate_c_instruction(instruction, line_num)
            machine_code.append(code)
        return machine_code

    def assemble(self, asm_path, output_hack_path=None, symbols_out_path=None):
        """Assembles an .asm file into .hack and outputs symbols.txt."""
        with open(asm_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        cleaned_instructions = self.first_pass(lines)
        machine_code = self.second_pass(cleaned_instructions)

        if not output_hack_path:
            base, _ = os.path.splitext(asm_path)
            output_hack_path = base + '.hack'

        with open(output_hack_path, 'w', encoding='utf-8') as f:
            for code in machine_code:
                f.write(code + '\n')

        # Personalized Feature: K % 3 == 0 -> Output symbols.txt
        if self.k % 3 == 0:
            if not symbols_out_path:
                asm_dir = os.path.dirname(os.path.abspath(output_hack_path))
                symbols_out_path = os.path.join(asm_dir, 'symbols.txt')
            with open(symbols_out_path, 'w', encoding='utf-8') as f:
                f.write("# Symbol Table (Resolved Addresses)\n")
                f.write("# Format: SymbolName -> Address (Dec / Hex)\n")
                f.write("-" * 45 + "\n")
                for sym, addr in sorted(self.symbol_table.items(), key=lambda x: (x[1], x[0])):
                    f.write(f"{sym:<20} {addr:>6}  (0x{addr:04X})\n")

        return machine_code, output_hack_path, symbols_out_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <source.asm> [output.hack]")
        sys.exit(1)

    asm_file = sys.argv[1]
    out_hack = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isfile(asm_file):
        print(f"Error: File '{asm_file}' not found.")
        sys.exit(1)

    assembler = HackAssembler(k=30)
    try:
        code, hack_path, sym_path = assembler.assemble(asm_file, out_hack)
        print(f"Assembly successful: '{asm_file}' -> '{hack_path}' ({len(code)} instructions)")
        if sym_path and os.path.exists(sym_path):
            print(f"Symbol table generated: '{sym_path}'")
    except Exception as e:
        print(f"Assembly Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
