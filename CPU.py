import sys
import random
from GPU import GPU


class CPU:
    def __init__(self):
        self.memory = [0] * 4096
        self.pause = False
        try:
            try:
                pixel_size = int(sys.argv[2])
            except ValueError:
                print("Error: Incorrect pixel size")
                exit()
        except IndexError:
            pixel_size = 20
        self.gpu = GPU(pixel_size)
        self.gpu.master.title("CHIP-8 Emulator")
        self.gpu.master.bind("<KeyPress>", self.on_key_down)
        self.gpu.master.bind("<KeyRelease>", self.on_key_up)
        self.gpu.master.bind("<space>", self.invert_pause)
        self.gpu.master.bind("<Escape>", self.exit_program)
        self.pc = 0x200  # Pointer counter
        self.read_instructions()
        self.opcode = 0
        self.stack = []
        self.registers = {0x0: 0,
                          0x1: 0,
                          0x2: 0,
                          0x3: 0,
                          0x4: 0,
                          0x5: 0,
                          0x6: 0,
                          0x7: 0,
                          0x8: 0,
                          0x9: 0,
                          0xa: 0,
                          0xb: 0,
                          0xc: 0,
                          0xd: 0,
                          0xe: 0,
                          0xf: 0}
        self.ir = 0  # Index register
        self.delay_timer = 0
        self.sound_timer = 0
        self.opcode_functions_map = {0x0000: self._0NNN,
                                     0x1000: self._1NNN,
                                     0x2000: self._2NNN,
                                     0x3000: self._3XNN,
                                     0x4000: self._4XNN,
                                     0x5000: self._5XY0,
                                     0x6000: self._6XNN,
                                     0x7000: self._7XNN,
                                     0x8000: self._8XYN,
                                     0x9000: self._9XY0,
                                     0xa000: self._ANNN,
                                     0xb000: self._BNNN,
                                     0xc000: self._CXNN,
                                     0xd000: self._DXYN,
                                     0xe000: self._EXNN,
                                     0xf000: self._FXNN}
        self.key_bind = {49: 0x1,  # Key 1
                         50: 0x2,  # Key 2
                         51: 0x3,  # Key 3
                         52: 0xc,  # Key C
                         81: 0x4,  # Key 4
                         87: 0x5,  # Key 5
                         69: 0x6,  # Key 6
                         82: 0xd,  # Key D
                         65: 0x7,  # Key 7
                         83: 0x8,  # Key 8
                         68: 0x9,  # Key 9
                         70: 0xe,  # Key E
                         90: 0xa,  # Key A
                         88: 0x0,  # Key 0
                         67: 0xb,  # Key B
                         86: 0xf}  # Key F
        self.key_state = {0x1: False,  # Key 1
                          0x2: False,  # Key 2
                          0x3: False,  # Key 3
                          0xc: False,  # Key C
                          0x4: False,  # Key 4
                          0x5: False,  # Key 5
                          0x6: False,  # Key 6
                          0xd: False,  # Key D
                          0x7: False,  # Key 7
                          0x8: False,  # Key 8
                          0x9: False,  # Key 9
                          0xe: False,  # Key E
                          0xa: False,  # Key A
                          0x0: False,  # Key 0
                          0xb: False,  # Key B
                          0xf: False}  # Key F
        #
        # |1|2|3|C|                         |1|2|3|4|
        # |4|5|6|D|  <= original keypad     |Q|W|E|R|
        # |7|8|9|E|  is equivalent as       |A|S|D|F|
        # |A|0|B|F|  keys on keyboard =>    |Z|X|C|V|
        #
        self.fonts = [0xf0, 0x90, 0x90, 0x90, 0xf0,  # 0
                      0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                      0xf0, 0x10, 0xf0, 0x80, 0xf0,  # 2
                      0xf0, 0x10, 0xf0, 0x10, 0xf0,  # 3
                      0x90, 0x90, 0xf0, 0x10, 0x10,  # 4
                      0xf0, 0x80, 0xf0, 0x10, 0xf0,  # 5
                      0xf0, 0x80, 0xf0, 0x90, 0xf0,  # 6
                      0xf0, 0x10, 0x20, 0x40, 0x40,  # 7
                      0xf0, 0x90, 0xf0, 0x90, 0xf0,  # 8
                      0xf0, 0x90, 0xf0, 0x10, 0xf0,  # 9
                      0xf0, 0x90, 0xf0, 0x90, 0x90,  # A
                      0xe0, 0x90, 0xe0, 0x90, 0xe0,  # B
                      0xf0, 0x80, 0x80, 0x80, 0xf0,  # C
                      0xe0, 0x90, 0x90, 0x90, 0xe0,  # D
                      0xf0, 0x80, 0xf0, 0x80, 0xf0,  # E
                      0xf0, 0x80, 0xf0, 0x80, 0x80]  # F
        self.load_fonts()
        self.timer_speed = 20  # Timer speed. The less the faster. Recommended is 20
        self.draw_speed = 1  # Speed of drawing updating. The less the faster. Recommended between 1 and 7

    def main(self):
        self.gpu.main()
        self.cycle()
        self.timers_cycle()
        self.gpu.master.mainloop()

    def cycle(self):
        """
        Cyclically gets new opcode from memory and executes it
        """
        if not self.pause:
            self.get_opcode()
            self.execute_opcode()
            self.gpu.master.update()
        self.gpu.master.after(self.draw_speed, self.cycle)

    def timers_cycle(self):
        """
        Updates timers values
        """
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            # Beeping here
        self.gpu.master.after(self.timer_speed, self.timers_cycle)

    def read_instructions(self):
        """
        Read instructions from file and write them to memory
        """
        try:
            filename = sys.argv[1]
        except IndexError:
            return
        with open(filename, "rb") as game:
            byte = game.read(1)
            i = 0
            while byte:
                self.memory[self.pc + i] = ord(byte)
                byte = game.read(1)
                i += 1

    def get_opcode(self):
        """
        Uses magic to get opcode from memory
        """
        self.opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2

    def execute_opcode(self):
        """
        Executing opcode
        """
        try:
            self.opcode_functions_map[self.opcode & 0xf000]()
        except KeyError:
            print("UNKNOWN OPCODE", self.opcode)

    def on_key_down(self, key):
        """
        Changes the key state to down
        """
        if key.keycode in self.key_bind:
            self.key_state[self.key_bind[key.keycode]] = True

    def on_key_up(self, key):
        """
        Changes the key state to up
        """
        if key.keycode in self.key_bind:
            self.key_state[self.key_bind[key.keycode]] = False

    def load_fonts(self):
        """
        Load system fonts to memory
        """
        for i in range(len(self.fonts)):
            self.memory[i] = self.fonts[i]

    def invert_pause(self, key):
        self.pause = not self.pause

    def exit_program(self, key):
        self.gpu.master.destroy()

    def _0NNN(self):
        """
        Executing opcode started with 0
        """
        opcode_0 = self.opcode & 0x00ff
        opcode_0_function_map = {0x00e0: self._00E0,
                                 0x00ee: self._00EE}
        opcode_0_function_map[opcode_0]()

    def _00E0(self):
        """
        Clears the screen
        """
        self.gpu.clear_screen()

    def _00EE(self):
        """
        Returns from a subroutine
        """
        self.pc = self.stack.pop()

    def _1NNN(self):
        """
        Jumps to address NNN
        """
        self.pc = (self.opcode & 0x0fff)

    def _2NNN(self):
        """
        Calls subroutine at NNN
        """
        self.stack.append(self.pc)
        self.pc = (self.opcode & 0x0fff)

    def _3XNN(self):
        """
        Skips the next instruction if register X equals NN
        """
        if self.registers[(self.opcode & 0x0f00) >> 8] == (self.opcode & 0x00ff):
            self.pc += 2

    def _4XNN(self):
        """
        Skips the next instruction if register X doesn't equal NN
        """
        if self.registers[(self.opcode & 0x0f00) >> 8] != (self.opcode & 0x00ff):
            self.pc += 2

    def _5XY0(self):
        """
        Skips the next instruction if register X equals register Y
        """
        if self.registers[(self.opcode & 0x0f00) >> 8] == self.registers[(self.opcode & 0x00f0) >> 4]:
            self.pc += 2

    def _6XNN(self):
        """
        Sets register X to NN
        """
        self.registers[(self.opcode & 0x0f00) >> 8] = (self.opcode & 0x00ff)

    def _7XNN(self):
        """
        Adds NN to register X
        """
        self.registers[(self.opcode & 0x0f00) >> 8] += (self.opcode & 0x00ff)
        self.registers[(self.opcode & 0x0f00) >> 8] &= 0x00ff

    def _8XYN(self):
        """
        Executing opcode started with 8
        """
        opcode_8 = self.opcode & 0xf00f
        opcode_8_function_map = {0x8000: self._8XY0,
                                 0x8001: self._8XY1,
                                 0x8002: self._8XY2,
                                 0x8003: self._8XY3,
                                 0x8004: self._8XY4,
                                 0x8005: self._8XY5,
                                 0x8006: self._8XY6,
                                 0x8007: self._8XY7,
                                 0x800e: self._8XYE}
        opcode_8_function_map[opcode_8]()

    def _8XY0(self):
        """
        Sets register X to register Y
        """
        self.registers[(self.opcode & 0x0f00) >> 8] = self.registers[(self.opcode & 0x00f0) >> 4]

    def _8XY1(self):
        """
        Sets register X to register X or register Y
        """
        self.registers[(self.opcode & 0x0f00) >> 8] |= self.registers[(self.opcode & 0x00f0) >> 4]

    def _8XY2(self):
        """
        Sets register X to register X and register Y
        """
        self.registers[(self.opcode & 0x0f00) >> 8] &= self.registers[(self.opcode & 0x00f0) >> 4]

    def _8XY3(self):
        """
        Sets register X to register X xor register Y
        """
        self.registers[(self.opcode & 0x0f00) >> 8] ^= self.registers[(self.opcode & 0x00f0) >> 4]

    def _8XY4(self):
        """
        Adds register Y to register X. Register F is set to 1 when there's a carry, and to 0 when there isn't
        """
        self.registers[(self.opcode & 0x0f00) >> 8] += self.registers[(self.opcode & 0x00f0) >> 4]
        if self.registers[(self.opcode & 0x0f00) >> 8] > 0xff:
            self.registers[0xf] = 1
            self.registers[(self.opcode & 0x0f00) >> 8] &= 0xff
        else:
            self.registers[0xf] = 0

    def _8XY5(self):
        """
        Register Y is subtracted from register X. Register F is set to 0 when there's a borrow, and 1 when there isn't
        """
        self.registers[(self.opcode & 0x0f00) >> 8] -= self.registers[(self.opcode & 0x00f0) >> 4]
        if self.registers[(self.opcode & 0x0f00) >> 8] > 0:
            self.registers[0xf] = 1
        else:
            self.registers[0xf] = 0
        self.registers[(self.opcode & 0x0f00) >> 8] &= 0xff

    def _8XY6(self):
        """
        Shifts register Y right by one and stores the result to register X.
        Register F is set to the value of the least significant bit of register Y before the shift
        """
        self.registers[0xf] = self.registers[(self.opcode & 0x0f00) >> 8] & 0x1
        self.registers[(self.opcode & 0x0f00) >> 8] = self.registers[(self.opcode & 0x0f00) >> 8] >> 1

    def _8XY7(self):
        """
        Sets register X to register Y minus register X.
        Register F is set to 0 when there's a borrow, and 1 when there isn't
        """
        self.registers[(self.opcode & 0x0f00) >> 8] = self.registers[(self.opcode & 0x00f0) >> 4] - self.registers[
            (self.opcode & 0x0f00) >> 8]
        if self.registers[(self.opcode & 0x0f00) >> 8] > 0:
            self.registers[0xf] = 1
        else:
            self.registers[0xf] = 0
        self.registers[(self.opcode & 0x0f00) >> 8] &= 0xff

    def _8XYE(self):
        """
        Shifts register Y left by one and copies the result to register X.
        Register F is set to the value of the most significant bit of register Y before the shift
        """
        self.registers[0xf] = self.registers[(self.opcode & 0x0f00) >> 8] & 0x1
        self.registers[(self.opcode & 0x0f00) >> 8] = self.registers[(self.opcode & 0x0f00) >> 8] << 1

    def _9XY0(self):
        """
        Skips the next instruction if register X doesn't equal register Y
        """
        if self.registers[(self.opcode & 0x0f00) >> 8] != self.registers[(self.opcode & 0x00f0) >> 4]:
            self.pc += 2

    def _ANNN(self):
        """
        Sets Index Register to the address NNN
        """
        self.ir = (self.opcode & 0x0fff)

    def _BNNN(self):
        """
        Jumps to the address NNN plus register 0
        """
        self.pc = (self.opcode & 0x0fff) + self.registers[0x0]

    def _CXNN(self):
        """
        Sets register X to the result of a bitwise and operation on a random number (from 0 to 255) and N
        """
        self.registers[(self.opcode & 0x0f00) >> 8] = (random.randint(0, 255) & (self.opcode & 0x00ff))

    def _DXYN(self):
        """
        Draws a sprite at coordinate (register X, register Y) that has a width of 8 pixels and a height of N pixels.
        Each row of 8 pixels is read as bit-coded starting from memory location Instruction Register.
        Register F is set to 1 if any screen pixels are flipped from set to unset when the sprite is drawn,
        and to 0 if that doesn’t happen
        """
        sprite = []
        for i in range(0, self.opcode & 0x000f):
            sprite.append(bin(self.memory[self.ir + i])[2:].zfill(8))
        self.registers[0xf] = self.gpu.draw_sprite(self.registers[(self.opcode & 0x0f00) >> 8],
                                                   self.registers[(self.opcode & 0x00f0) >> 4], sprite)

    def _EXNN(self):
        """
        Executing opcode started with E
        """
        opcode_e = (self.opcode & 0xf0ff)
        opcode_e_function_map = {0xe09e: self._EX9E,
                                 0xe0a1: self._EXA1}
        opcode_e_function_map[opcode_e]()

    def _EX9E(self):
        """
        Skips the next instruction if the key stored in register X is pressed
        """
        if self.key_state[self.registers[(self.opcode & 0x0f00) >> 8]]:
            self.pc += 2

    def _EXA1(self):
        """
        Skips the next instruction if the key stored in register X isn't pressed
        """
        if not (self.key_state[self.registers[(self.opcode & 0x0f00) >> 8]]):
            self.pc += 2

    def _FXNN(self):
        """
        Executing opcode started with E
        """
        opcode_f = (self.opcode & 0xf0ff)
        opcode_f_function_map = {0xf007: self._FX07,
                                 0xf00a: self._FX0A,
                                 0xf015: self._FX15,
                                 0xf018: self._FX18,
                                 0xf01e: self._FX1E,
                                 0xf029: self._FX29,
                                 0xf033: self._FX33,
                                 0xf055: self._FX55,
                                 0xf065: self._FX65}
        opcode_f_function_map[opcode_f]()

    def _FX07(self):
        """
        Sets register X to the value of the delay timer
        """
        self.registers[(self.opcode & 0x0f00) >> 8] = self.delay_timer

    def _FX0A(self):
        """
        A key press is awaited, and then stored in register X
        """
        key_pressed = False
        for key in range(len(self.key_state)):
            if self.key_state[key]:
                self.registers[(self.opcode & 0x0f00) >> 8] = key
                key_pressed = True
                break
        if not key_pressed:
            self.pc -= 2

    def _FX15(self):
        """
        Sets the delay timer to register X
        """
        self.delay_timer = self.registers[(self.opcode & 0x0f00) >> 8]

    def _FX18(self):
        """
        Sets the sound timer to register X
        """
        self.sound_timer = self.registers[(self.opcode & 0x0f00) >> 8]

    def _FX1E(self):
        """
        Adds register X to Instruction Register
        """
        self.ir += self.registers[(self.opcode & 0x0f00) >> 8]

    def _FX29(self):
        """
        Sets Instruction Register to the location of the sprite for the character in register X
        """
        self.ir = (5 * self.registers[(self.opcode & 0x0f00) >> 8])

    def _FX33(self):
        """
        Takes the decimal representation of register X,
        places the hundreds digit in memory at location in Instruction Register,
        the tens digit at location Instruction Register + 1,
        and the ones digit at location Instruction Register + 2
        """
        self.memory[self.ir] = int(self.registers[(self.opcode & 0x0F00) >> 8] / 100)
        self.memory[self.ir + 1] = int((self.registers[(self.opcode & 0x0F00) >> 8] % 100) / 10)
        self.memory[self.ir + 2] = int(self.registers[(self.opcode & 0x0F00) >> 8] % 10)

    def _FX55(self):
        """
        Stores registers from 0 to X (including X) in memory starting at address stored in Instruction Register.
        """
        for i in range(((self.opcode & 0x0F00) >> 8) + 1):
            self.memory[self.ir + i] = self.registers[i]

    def _FX65(self):
        """
        Fills registers from 0 to X (including X) with values
        from memory starting at address stored in Instruction Register
        """
        for i in range(((self.opcode & 0x0F00) >> 8) + 1):
            self.registers[i] = self.memory[self.ir + i]
