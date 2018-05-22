import unittest
from CPU import CPU


class CPUTests(unittest.TestCase):

    def setUp(self):
        self.cpu = CPU("tkinter")

    def test_00E0(self):
        self.cpu.opcode = 0x00e0
        self.cpu.gpu.memory[0][0] = 1
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.gpu.memory[0][0], 0)

    def test_00EE(self):
        self.cpu.stack.append(0x1234)
        self.cpu._00EE()
        self.assertEqual(self.cpu.pc, 0x1234)

    def test_1NNN(self):
        self.cpu.opcode = 0x1234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x234)

    def test_2NNN(self):
        self.cpu.opcode = 0x22d4
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.stack.pop(), 0x200)
        self.assertEqual(self.cpu.pc, 0x02d4)

    def test_3XNN_1(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x34
        self.cpu.opcode = 0x3234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x2)

    def test_3XNN_2(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x35
        self.cpu.opcode = 0x3234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)

    def test_4XNN_1(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x34
        self.cpu.opcode = 0x4234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)

    def test_4XNN_2(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x35
        self.cpu.opcode = 0x4234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x2)

    def test_5XY0_1(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x4
        self.cpu.registers[0x3] = 0x4
        self.cpu.opcode = 0x5230
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x2)

    def test_5XY0_2(self):
        self.cpu.pc = 0x0
        self.cpu.registers[0x2] = 0x4
        self.cpu.registers[0x3] = 0x5
        self.cpu.opcode = 0x5230
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)

    def test_6XNN(self):
        self.cpu.opcode = 0x6a02
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0xa], 0x02)

    def test_7XNN(self):
        self.cpu.registers[0x1] = 0x1f
        self.cpu.opcode = 0x71ff
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x1], 0x1e)

    def test_8XY0(self):
        self.cpu.registers[0x2] = 0x2
        self.cpu.registers[0x3] = 0x3
        self.cpu.opcode = 0x8230
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x3)

    def test_8XY1(self):
        self.cpu.registers[0x2] = 0x2200
        self.cpu.registers[0x3] = 0x0033
        self.cpu.opcode = 0x8231
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x2233)

    def test_8XY2(self):
        self.cpu.registers[0x2] = 0x2200
        self.cpu.registers[0x3] = 0x0033
        self.cpu.opcode = 0x8232
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x0)

    def test_8XY3(self):
        self.cpu.registers[0x2] = 0x3
        self.cpu.registers[0x3] = 0x5
        self.cpu.opcode = 0x8233
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x6)

    def test_8XY4_1(self):
        self.cpu.registers[0x2] = 0x22
        self.cpu.registers[0x3] = 0x33
        self.cpu.opcode = 0x8234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x55)
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_8XY4_2(self):
        self.cpu.registers[0x2] = 0xff
        self.cpu.registers[0x3] = 0xff
        self.cpu.opcode = 0x8234
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0xfe)
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_8XY5_1(self):
        self.cpu.registers[0x2] = 0xff
        self.cpu.registers[0x3] = 0xff
        self.cpu.opcode = 0x8235
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x0)
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_8XY5_2(self):
        self.cpu.registers[0x2] = 0xff
        self.cpu.registers[0x3] = 0xfe
        self.cpu.opcode = 0x8235
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x1)
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_8XY6_1(self):
        self.cpu.registers[0x2] = 0x4
        self.cpu.opcode = 0x8236
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x2)
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_8XY6_2(self):
        self.cpu.registers[0x2] = 0x3
        self.cpu.opcode = 0x8236
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x1)
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_8XY7_1(self):
        self.cpu.registers[0x2] = 0xfe
        self.cpu.registers[0x3] = 0xff
        self.cpu.opcode = 0x8237
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x1)
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_8XY7_2(self):
        self.cpu.registers[0x2] = 0xff
        self.cpu.registers[0x3] = 0xff
        self.cpu.opcode = 0x8237
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x0)
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_8XYE_1(self):
        self.cpu.registers[0x2] = 0x2
        self.cpu.opcode = 0x823e
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x4)
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_8XYE_2(self):
        self.cpu.registers[0x2] = 0x3
        self.cpu.opcode = 0x823e
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x6)
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_9XY0_1(self):
        self.cpu.registers[0x2] = 0x2
        self.cpu.registers[0x3] = 0x2
        self.cpu.pc = 0
        self.cpu.opcode = 0x9230
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0)

    def test_9XY0_2(self):
        self.cpu.registers[0x2] = 0x2
        self.cpu.registers[0x3] = 0x3
        self.cpu.pc = 0
        self.cpu.opcode = 0x9230
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 2)

    def test_ANNN(self):
        self.cpu.opcode = 0xa2ea
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.ir, 0x02ea)

    def test_BNNN(self):
        self.cpu.registers[0x0] = 2
        self.cpu.pc = 3
        self.cpu.opcode = 0xb004
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x6)

    def test_DXYN_1(self):
        self.cpu.ir = 0
        self.cpu.memory[0x0] = 0xff
        self.cpu.registers[0x5] = 0x5
        self.cpu.registers[0x6] = 0x5
        self.cpu.opcode = 0xd561
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_DXYN_2(self):
        self.cpu.ir = 0
        self.cpu.memory[0x0] = 0xff
        self.cpu.registers[0x5] = 0x5
        self.cpu.registers[0x6] = 0x5
        self.cpu.opcode = 0xd561
        self.cpu.execute_opcode()
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0xf], 0x1)

    def test_DXYN_3(self):
        self.cpu.ir = 0
        self.cpu.memory[0x0] = 0x0
        self.cpu.registers[0x5] = 0x5
        self.cpu.registers[0x6] = 0x5
        self.cpu.opcode = 0xd561
        self.cpu.execute_opcode()
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0xf], 0x0)

    def test_EX9E_1(self):
        self.cpu.key_state[0x2] = True
        self.cpu.pc = 0
        self.cpu.registers[0x3] = 0x2
        self.cpu.opcode = 0xe39e
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x2)

    def test_EX9E_2(self):
        self.cpu.key_state[0x2] = False
        self.cpu.pc = 0
        self.cpu.registers[0x3] = 0x2
        self.cpu.opcode = 0xe39e
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)

    def test_EXA1_1(self):
        self.cpu.key_state[0x2] = False
        self.cpu.pc = 0
        self.cpu.registers[0x3] = 0x2
        self.cpu.opcode = 0xe3a1
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x2)

    def test_EXA1_2(self):
        self.cpu.key_state[0x2] = True
        self.cpu.pc = 0
        self.cpu.registers[0x3] = 0x2
        self.cpu.opcode = 0xe3a1
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)

    def test_FX07(self):
        self.cpu.delay_timer = 0x5
        self.cpu.registers[0x2] = 0x0
        self.cpu.opcode = 0xf207
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x5)

    def test_FX0A(self):
        self.cpu.registers[0x2] = 0x5
        self.cpu.pc = 0x2
        self.cpu.opcode = 0xf20a
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.pc, 0x0)
        self.cpu.key_state[0x8] = True
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x2], 0x8)

    def test_FX15(self):
        self.cpu.delay_timer = 0x5
        self.cpu.registers[0x2] = 0x7
        self.cpu.opcode = 0xf215
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.delay_timer, 0x7)

    def test_FX18(self):
        self.cpu.registers[0x2] = 0x5
        self.cpu.sound_timer = 0x2
        self.cpu.opcode = 0xf218
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.sound_timer, 0x5)

    def test_FX1E(self):
        self.cpu.ir = 0x5
        self.cpu.registers[0x2] = 0x4
        self.cpu.opcode = 0xf21e
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.ir, 0x9)

    def test_FX29(self):
        self.cpu.ir = 0x1234
        self.cpu.registers[0x2] = 0x4
        self.cpu.opcode = 0xf229
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.ir, 20)

    def test_FX33(self):
        self.cpu.registers[0x2] = 456
        self.cpu.ir = 0
        self.cpu.opcode = 0xf233
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.memory[0], 4)
        self.assertEqual(self.cpu.memory[1], 5)
        self.assertEqual(self.cpu.memory[2], 6)

    def test_FX55(self):
        self.cpu.registers[0x0] = 4
        self.cpu.registers[0x1] = 3
        self.cpu.registers[0x2] = 1
        self.cpu.registers[0x3] = 8
        self.cpu.ir = 0
        self.cpu.opcode = 0xf355
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.memory[0], 4)
        self.assertEqual(self.cpu.memory[1], 3)
        self.assertEqual(self.cpu.memory[2], 1)
        self.assertEqual(self.cpu.memory[3], 8)

    def test_FX65(self):
        self.cpu.memory[0] = 6
        self.cpu.memory[1] = 2
        self.cpu.memory[2] = 1
        self.cpu.memory[3] = 7
        self.cpu.memory[4] = 0
        self.cpu.ir = 0
        self.cpu.opcode = 0xf465
        self.cpu.execute_opcode()
        self.assertEqual(self.cpu.registers[0x0], 6)
        self.assertEqual(self.cpu.registers[0x1], 2)
        self.assertEqual(self.cpu.registers[0x2], 1)
        self.assertEqual(self.cpu.registers[0x3], 7)
        self.assertEqual(self.cpu.registers[0x4], 0)

    def test_get_opcode(self):
        self.cpu.pc = 0x0
        self.cpu.memory[0x0] = 0x12
        self.cpu.memory[0x1] = 0x34
        self.cpu.get_opcode()
        self.assertEqual(self.cpu.opcode, 0x1234)



if __name__ == "__main__":
    unittest.main()
