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
        opcode_setup(0x10, 0xFF)
        cpu.decode()

        assert cpu.pc == 0xFF 

    def test_6nnn(self):
        # set Vx = kk
        cpu = CPU()
        cpu.initialize_cpu()

        cpu.memory[0] = 