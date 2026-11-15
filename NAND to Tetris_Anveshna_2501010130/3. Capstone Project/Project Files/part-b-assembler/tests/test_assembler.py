"""
Unit and integration tests for HackAssembler.
Verifies parsing, symbol table resolution, A-instruction, C-instruction translation,
error handling, and the personalized feature (K=30, K%3=0 -> symbols.txt).
"""

import unittest
import os
import sys
import tempfile
import shutil

# Ensure assembler module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from assembler import HackAssembler, PREDEFINED_SYMBOLS


class TestHackAssembler(unittest.TestCase):
    def setUp(self):
        self.assembler = HackAssembler(k=30)
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_clean_line(self):
        self.assertEqual(self.assembler.clean_line("   @2 // load constant 2   "), "@2")
        self.assertEqual(self.assembler.clean_line("// entire line comment"), "")
        self.assertEqual(self.assembler.clean_line("   D=M+1   "), "D=M+1")

    def test_a_instruction_numeric(self):
        code = self.assembler.translate_a_instruction("@0", 1)
        self.assertEqual(code, "0000000000000000")
        code = self.assembler.translate_a_instruction("@21", 2)
        self.assertEqual(code, "0000000000010101")
        code = self.assembler.translate_a_instruction("@16384", 3)
        self.assertEqual(code, "0100000000000000")

    def test_predefined_symbols(self):
        self.assertEqual(self.assembler.translate_a_instruction("@SCREEN", 1), "0100000000000000")
        self.assertEqual(self.assembler.translate_a_instruction("@KBD", 2), "0110000000000000")
        self.assertEqual(self.assembler.translate_a_instruction("@SP", 3), "0000000000000000")
        self.assertEqual(self.assembler.translate_a_instruction("@R15", 4), "0000000000001111")

    def test_c_instruction(self):
        # D=M+1 -> 111 1 110111 010 000
        self.assertEqual(self.assembler.translate_c_instruction("D=M+1", 1), "1111110111010000")
        # 0;JMP -> 111 0 101010 000 111
        self.assertEqual(self.assembler.translate_c_instruction("0;JMP", 2), "1110101010000111")
        # MD=D-1 -> 111 0 001110 011 000
        self.assertEqual(self.assembler.translate_c_instruction("MD=D-1", 3), "1110001110011000")

    def test_variable_allocation(self):
        code1 = self.assembler.translate_a_instruction("@varA", 1)
        code2 = self.assembler.translate_a_instruction("@varB", 2)
        code1_repeat = self.assembler.translate_a_instruction("@varA", 3)
        self.assertEqual(code1, "0000000000010000")  # RAM[16]
        self.assertEqual(code2, "0000000000010001")  # RAM[17]
        self.assertEqual(code1_repeat, "0000000000010000")

    def test_label_resolution(self):
        lines = [
            "// Simple loop",
            "@counter",
            "M=0",
            "(LOOP)",
            "@counter",
            "M=M+1",
            "@LOOP",
            "0;JMP"
        ]
        cleaned = self.assembler.first_pass(lines)
        code = self.assembler.second_pass(cleaned)
        # @LOOP is at ROM instruction index 2
        loop_jump_instruction = code[4]
        self.assertEqual(loop_jump_instruction, "0000000000000010")

    def test_personalized_symbols_generation(self):
        asm_content = """
        @i
        M=1
        (LOOP)
        @i
        D=M
        @LOOP
        0;JMP
        """
        asm_path = os.path.join(self.test_dir, "test.asm")
        hack_path = os.path.join(self.test_dir, "test.hack")
        sym_path = os.path.join(self.test_dir, "symbols.txt")
        with open(asm_path, "w") as f:
            f.write(asm_content)

        self.assembler.assemble(asm_path, hack_path, sym_path)
        self.assertTrue(os.path.exists(hack_path))
        self.assertTrue(os.path.exists(sym_path))

        with open(sym_path) as f:
            sym_text = f.read()
        self.assertIn("LOOP", sym_text)
        self.assertIn("i", sym_text)
        self.assertIn("SCREEN", sym_text)


if __name__ == "__main__":
    unittest.main()
