import pytest
from emulator.cpu import CPU, fonts


def opcode_setup(o1, o2):
    cpu = CPU()
    cpu.initialize_cpu()

    cpu.memory[0x200] = o1
    cpu.memory[0x200+1] = o2
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
        # clear screen
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

    def test_00EE(self):
        # return from a suboutine
        cpu = opcode_setup(0x00, 0xEE)

        cpu.stack[0] = 0x500
        cpu.sp = 1

        cpu.decode()

        assert cpu.pc == 0x500
        assert cpu.sp == 0

    def test_1nnn(self):
        # jump to addr nnn
        cpu = opcode_setup(0x10, 0xFF)
        cpu.decode()

        cpu2 = opcode_setup(0x12, 0x28)
        cpu2.decode()

        assert cpu.pc == 0xFF 
        assert cpu2.pc == 0x228

    def test_2nnn(self):
        # call subroutine at nnn
        cpu = opcode_setup(0x23, 0x45)
        cpu.decode()

        assert cpu.pc == 0x345
        assert cpu.stack[0] == 0x200
        assert cpu.sp == 1

    def test_3xkk(self):
        # if Vx == kk, skip next inst
        cpu = opcode_setup(0x31, 0x45)
        cpu.V[1] = 0x45
        cpu.decode()

        assert cpu.pc == 0x204

        cpu = opcode_setup(0x31, 0x45)
        cpu.V[1] = 0x00
        cpu.decode()

        assert cpu.pc == 0x202

    def test_4xkk(self):
        # if Vx != kk, skip next inst
        cpu = opcode_setup(0x41, 0x45)
        cpu.V[1] = 0x45
        cpu.decode()

        assert cpu.pc == 0x202

        cpu = opcode_setup(0x41, 0x45)
        cpu.V[1] = 0x00
        cpu.decode()

        assert cpu.pc == 0x204

    def test_5xy0(self):
        # if Vx == Vy, skip next inst
        cpu = opcode_setup(0x51, 0x40)
        cpu.V[1] = 1
        cpu.V[4] = 1
        cpu.decode()

        assert cpu.pc == 0x204

        cpu = opcode_setup(0x51, 0x40)
        cpu.V[1] = 1
        cpu.V[4] = 2
        cpu.decode()

        assert cpu.pc == 0x202

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

    def test_8xy0(self):
        # set Vx = Vy
        cpu = opcode_setup(0x84, 0x50)
        cpu.V[4] = 4
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[1] == cpu.V[2]

    def test_8xy1(self):
        # set Vx = (Vx OR Vy)
        cpu = opcode_setup(0x84, 0x51)
        cpu.V[4] = 4
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == (4 | 5)

    def test_8xy2(self):
        # set Vx = (Vx AND Vy)
        cpu = opcode_setup(0x84, 0x52)
        cpu.V[4] = 4
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == (4 & 5)

    def test_8xy3(self):
        # set Vx = (Vx XOR Vy)
        cpu = opcode_setup(0x84, 0x53)
        cpu.V[4] = 4
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == (4 ^ 5)

    def test_8xy4(self):
        # set Vx = (Vx + Vy), set VF = carry
        cpu = opcode_setup(0x84, 0x54)
        cpu.V[4] = 4
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == (4 + 5)
        assert cpu.V[0xF] == 0

        cpu = opcode_setup(0x84, 0x54)
        cpu.V[4] = 250
        cpu.V[5] = 50
        cpu.decode()

        assert cpu.V[4] == 250 + 50 - 255
        assert cpu.V[0xF] == 1

    def test_8xy5(self):
        # set Vx = (Vx - Vy), set VF = NOT borrow
        cpu = opcode_setup(0x84, 0x55)
        cpu.V[4] = 5
        cpu.V[5] = 10
        cpu.decode()

        assert cpu.V[4] == 250
        assert cpu.V[0xF] == 0

        cpu = opcode_setup(0x84, 0x55)
        cpu.V[4] = 10
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == 10 - 5
        assert cpu.V[0xF] == 1

    def test_8xy6(self):
        # set Vx = Vy SHR 1
        cpu = opcode_setup(0x84, 0x56)
        cpu.V[4] = 41
        cpu.decode()

        assert cpu.V[4] == 41 >> 1
        assert cpu.V[0xF] == 1

        cpu = opcode_setup(0x84, 0x56)
        cpu.V[4] = 40
        cpu.decode()

        assert cpu.V[4] == 40 >> 1
        assert cpu.V[0xF] == 0

    def test_8xy7(self):
        # set Vx = (Vy - Vx), set VF = NOT borrow
        # test vy > vx
        cpu = opcode_setup(0x84, 0x57)
        cpu.V[4] = 5
        cpu.V[5] = 10
        cpu.decode()

        assert cpu.V[4] == 10 - 5
        assert cpu.V[0xF] == 1

        # test vy <= vx
        cpu = opcode_setup(0x84, 0x57)
        cpu.V[4] = 10
        cpu.V[5] = 5
        cpu.decode()

        assert cpu.V[4] == 255 + (5 - 10)
        assert cpu.V[0xF] == 0

    def test_8xyE(self):
        # set Vx = Vy SHR 1
        cpu = opcode_setup(0x84, 0x5E)
        cpu.V[4] = 128
        cpu.decode()

        assert cpu.V[4] == 128 << 1
        assert cpu.V[0xF] == 1

        cpu = opcode_setup(0x84, 0x5E)
        cpu.V[4] = 64
        cpu.decode()

        assert cpu.V[4] == 128  # 64 << 1
        assert cpu.V[0xF] == 0

    def test_9xy0(self):
        # if Vx != Vy, skip next inst
        cpu = opcode_setup(0x91, 0x40)
        cpu.V[1] = 1
        cpu.V[4] = 1
        cpu.decode()

        assert cpu.pc == 0x202

        cpu = opcode_setup(0x91, 0x45)
        cpu.V[1] = 1
        cpu.V[4] = 2
        cpu.decode()

        assert cpu.pc == 0x204

    def test_Annn(self):
        cpu = opcode_setup(0xA3, 0xFB)
        cpu.decode()
        assert cpu.I == 0x3FB

    def text_fx33(self):
        cpu = opcode_setup(0xF1, 0x33)
        cpu.V[1] = 156
        cpu.decode()

        assert cpu.memory[cpu.I] == 1
        assert cpu.memory[cpu.I+1] == 5
        assert cpu.memory[cpu.I+2] == 6

    def test_fx55(self):
        cpu = opcode_setup(0xF1, 0x55)
        cpu.I = 10
        for i in range(0xF):
            cpu.V[i] = i
        cpu.decode()

        for i in range(0xF):
            assert cpu.memory[cpu.I+i] == i

    def test_fx65(self):
        cpu = opcode_setup(0xF1, 0x65)
        cpu.I = 10
        for i in range(0xF):
            cpu.memory[10 + i] = i
        cpu.decode()

        for i in range(0xF):
            assert cpu.V[i] == i

    def test_fx1E(self):
        cpu = opcode_setup(0xF1, 0x1E)
        cpu.V[1] = 10
        cpu.I = 16
        cpu.decode()

        assert cpu.I == 10 + 16