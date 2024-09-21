import pytest
from emulator.cpu import CPU, fonts


def opcode_setup(o1, o2):
    cpu = CPU()
    cpu.initialize_cpu()

    cpu.memory[0] = o1
    cpu.memory[1] = o2
    return cpu


class TestCpu:
    def test_load_fonts(self):
        cpu = CPU()
        cpu.initialize_cpu()

        cpu.load_fonts()

        assert fonts == cpu.memory[0:len(fonts)]

    def test_load_rom(self):
        rom = [0x00, 0xE0, 0xA2, 0x2A, 0x60, 0x0C, 0x61, 0x08, 0xD0, 0x1F, 0x70, 0x09, 0xA2, 0x39, 0xD0, 0x1F, 0xA2, 0x48, 0x70, 0x08, 0xD0, 0x1F, 0x70, 0x04, 0xA2, 0x57, 0xD0, 0x1F, 0x70, 0x08, 0xA2, 0x66, 0xD0, 0x1F, 0x70, 0x08, 0xA2, 0x75, 0xD0, 0x1F, 0x12, 0x28, 0xFF, 0x00, 0xFF, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0x3C, 0x00, 0xFF, 0x00, 0xFF, 0xFF, 0x00, 0xFF, 0x00, 0x38, 0x00, 0x3F, 0x00, 0x3F, 0x00, 0x38, 0x00, 0xFF, 0x00, 0xFF, 0x80, 0x00, 0xE0, 0x00, 0xE0, 0x00, 0x80, 0x00, 0x80, 0x00, 0xE0, 0x00, 0xE0, 0x00, 0x80, 0xF8, 0x00, 0xFC, 0x00, 0x3E, 0x00, 0x3F, 0x00, 0x3B, 0x00, 0x39, 0x00, 0xF8, 0x00, 0xF8, 0x03, 0x00, 0x07, 0x00, 0x0F, 0x00, 0xBF, 0x00, 0xFB, 0x00, 0xF3, 0x00, 0xE3, 0x00, 0x43, 0xE0, 0x00, 0xE0, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0xE0, 0x00, 0xE0]
        cpu = CPU()
        cpu.initialize_cpu()
        cpu.load_rom("res/IBM_Logo.ch8")

        assert cpu.memory[0x200:0x200+len(rom)] == rom


    def test_fetch_opcode(self):
        cpu = CPU()
        cpu.initialize_cpu()

        start_index = 10
        cpu.pc = start_index
        cpu.memory[start_index] = 0x0E
        cpu.memory[start_index+1] = 0xE1
        assert cpu.fetch_opcode() == 0x0EE1
        assert cpu.pc == start_index + 2


class TestOpcode:
    def test_00E0(self):
        """ clear screen """
        cpu = CPU()
        cpu.initialize_cpu()

        display = []
        for y in range(32):
            display.append([])
            for x in range(64):
                display[y].append(0)
                cpu.display[y][x] = 1
        cpu.clear_screen()

        assert display == cpu.display

    def test_1nnn(self):
        # jump to addr nnn
        cpu = opcode_setup(0x10, 0xFF)
        cpu.decode()

        cpu2 = opcode_setup(0x12, 0x28)
        cpu2.decode()

        assert cpu.pc == 0xFF 
        assert cpu2.pc == 0x228

    def test_6xkk(self):
        # set Vx = kk
        cpu = opcode_setup(0x66, 0x13)
        cpu.decode()

        assert cpu.V[6] == 0x13

    def test_7xkk(self):
        # set Vx = Vx + kk
        cpu = opcode_setup(0x70, 0x13)
        cpu.V[0] = 5
        cpu.decode()
        assert cpu.V[0] == 5 + 0x13

    def test_Annn(self):
        cpu = opcode_setup(0xA3, 0xFB)
        cpu.decode()
        assert cpu.I == 0x3FB
