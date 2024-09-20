
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

    def update_timer(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def load_fonts(self):
        for i in range(len(fonts)):
            self.memory[i] = fonts[i]

    def fetch_opcode(self):
        byte_one = self.memory[self.pc]
        byte_two = self.memory[self.pc + 1]
        opcode = (byte_two << 8) | byte_one

        self.pc += 2
        return opcode
