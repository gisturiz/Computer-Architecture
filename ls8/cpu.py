"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ran_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            # Open file
            with open(filename) as f:
                # Read all the lines
                for line in f:
                    # Parse out comments
                    comment_split = line.strip().split("#")

                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()

                    # Ignore blank lines
                    if value == "":
                        continue

                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    if len(sys.argv) != 2:
        print("Error: Must have file name")
        sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while True:
            IR = self.ram[self.pc]

            operand_a = self.ram_read(self.pc + 1)  # register
            operand_b = self.ram_read(self.pc + 2)  # number

            LDI = 0b10000010
            MUL = 0b10100010
            PRN = 0b01000111
            HLT = 0b00000001

            if IR == LDI:
                register = operand_a
                num = operand_b
                self.reg[register] = num
                self.pc += 3
            elif IR == MUL or IR == ADD:
                op = IR
                reg1 = operand_a
                reg2 = operand_b
                self.alu(op, reg1, reg2)
                self.pc += 3
            elif IR == PUSH:
                register = operand_a
                val = self.reg[register]
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = val
                self.pc += 2
            elif IR == POP:
                register = operand_a
                val = self.ram[self.reg[self.SP]]
                self.reg[register] = val
                self.reg[self.SP] += 1
                self.pc += 2
            elif IR == CALL:
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = self.pc + 2
                register = operand_a
                self.pc = self.reg[register]
            elif IR == RET:
                self.pc = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
            elif IR == PRN:
                register = operand_a
                print(self.reg[register])
                self.pc += 2
            elif IR == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {IR}")
                sys.exit(1)
        
        self.trace()

class BranchTable(CPU):
    def __init__(self):
        super().__init__()
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[HLT] = self.handle_hlt
    
    def handle_ldi(self, a , b):
        # self.operand_a = a
        # self.operand_b = b
        self.reg[a] = b
        self.pc += 3

    def handle_mul(self, a, b):
        # self.operand_a = a
        # self.operand_b = b
        self.alu("MUL", a, b)
        self.pc += 3

    def handle_prn(self, a):
        # self.operand_a = a
        print(self.reg[a])
        self.pc += 2

    def handle_hlt(self):
        sys.exit(0)

    def run(self):

        IR = LDI
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.branchtable[IR](operand_a, operand_b)

        self.trace()

        IR = MUL
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.branchtable[IR](operand_a, operand_b)

        self.trace()

        IR = PRN
        operand_a = self.ram_read(self.pc + 1)
        self.branchtable[IR](operand_a)

        self.trace()

        IR = HLT
        self.branchtable[IR]
