import struct 
import logging

def merge_two_byte(b1, b2):
    return (b1 << 8) | b2

# CONST
MEMORY_SIZE = 4096
STACK_SIZE = 16
SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32
START_ADDR = 0x200

# font var
fonts = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
    0x20, 0x60, 0x20, 0x20, 0x70, # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
    0x90, 0x90, 0xF0, 0x10, 0x10, # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
    0xF0, 0x10, 0x20, 0x40, 0x40, # 7 
    0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90, # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
    0xF0, 0x80, 0x80, 0x80, 0xF0, # C
    0xE0, 0x90, 0x90, 0x90, 0xE0, # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
    0xF0, 0x80, 0xF0, 0x80, 0x80  # F
]


class CPU:
    def __init__(self):
        self.memory = [0] * MEMORY_SIZE
        self.pc = 0     # progress counter
        self.I = 0  # 16 bit
        self.stack = [0] * STACK_SIZE
        self.V = [0] * STACK_SIZE
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = []

    def initialize_cpu(self):
        self.memory = [0] * MEMORY_SIZE
        self.pc = 0     # progress counter
        self.I = 0  # 16 bit
        self.stack = [0] * STACK_SIZE
        self.V = [0] * STACK_SIZE
        self.delay_timer = 0
        self.sound_timer = 0
        self.init_display()

    def init_display(self):
        self.display = []

        for y in range(32):
            self.display.append([])
            for x in range(64):
                self.display[y].append(0)

    def clear_screen(self):
        for y in range(32):
            for x in range(64):
                self.display[y][x] = 0

    def update_timer(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def load_fonts(self):
        for i in range(len(fonts)):
            self.memory[i] = fonts[i]

    def load_rom(self, path):
        with open(path, 'rb') as f:
            binary_data = f.read()

        temp_array = struct.unpack(f'{len(binary_data)}B', binary_data)

        if (len(temp_array) + START_ADDR) > MEMORY_SIZE:
            print("Failed to load rom, file is too big.")

        for i in range(len(temp_array)):
            self.memory[START_ADDR + i] = temp_array[i]


    def fetch_opcode(self):
        byte_one = self.memory[self.pc]
        byte_two = self.memory[self.pc + 1]
        opcode = (byte_one << 8) | byte_two

        logging.debug(f"fetch(): pc({hex(self.pc)}) b1({hex(byte_one)}) b2({hex(byte_two)}) opcode({hex(opcode)})")

        self.pc += 2
        return opcode

    def decode(self):
        opcode = self.fetch_opcode()
        print(hex(opcode))

        n1 = (opcode >> 12) & 0xF
        n2 = (opcode >> 8) & 0xF
        n3 = (opcode >> 4) & 0xF
        n4 = opcode & 0xF

        logging.debug(f"n1({hex(n1)}) n2({hex(n2)}) n3({hex(n3)}) n4({hex(n4)}) op({hex(opcode)})")

        match n1:
            case 0x0:
                if n2 == 0x0 and n3 == 0xE and n4 == 0xE:
                    #0x00EE ret
                    pass
                elif n2 == 0x0 and n3 == 0xE:
                    logging.info(f"00E0 {hex(opcode)} CLS")
                    self.clear_screen()
                else:
                    # 0x0nnn sys addr
                    pass
            case 0x1:
                logging.info(f"1nnn {hex(opcode)} JP addr")
                self.pc = opcode & 0x0FFF
            case 0x6:
                logging.info(f"6xyk {hex(opcode)} LD Vx, Vy")
                self.V[n2] = opcode & 0x00FF
            case 0x7:
                logging.info(f"7xkk {hex(opcode)} ADD Vx, byte")
                self.V[n2] += opcode & 0x00FF
            case 0xA:
                logging.info(f"Annn {hex(opcode)} LD I, addr")
                self.I = opcode & 0x0FFF
            case 0xD:
                logging.info(f"Dxyn {hex(opcode)} DRW Vx, Vy, nibble")

                self.V[0xF] = 0
                y_pos = self.V[n3] % 32

                for row in range(n4):
                    x_pos = self.V[n2] % 64

                    sprite_byte = self.memory[self.I + row]
                    sprite_bits = bin(sprite_byte)[2:].zfill(8)

                    for bit in sprite_bits:
                        if bit == '1' and self.display[y_pos][x_pos] == 1:
                            self.display[y_pos][x_pos] = 0
                            self.V[0xF] = 1
                        elif bit == '1' and self.display[y_pos][x_pos] == 0:
                            self.display[y_pos][x_pos] = 1

                        x_pos += 1
                        if x_pos > 63:
                            break

                    y_pos += 1
                    if y_pos > 31:
                        break

            case _:
                pass
