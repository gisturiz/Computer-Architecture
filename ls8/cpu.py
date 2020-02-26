"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            print(self.reg[reg_a], self.reg[reg_b])
            self.reg[reg_a] *= self.reg[reg_b]
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
        ir = self.ram[self.pc]

        operand_a = self.ram_read(self.pc + 1)  # register
        operand_b = self.ram_read(self.pc + 2)  # number
        
        while True:
            command = self.ram[self.pc]

            LDI = 0b10000010
            MUL = 0b10100010
            PRN = 0b01000111
            HLT = 0b00000001

            if command == LDI:
                register = operand_a
                num = operand_b
                self.reg[register] = num
                self.pc += 3
            elif command == MUL:
                reg1 = operand_a
                reg2 = operand_b
                print(reg1, reg2)
                self.alu("MUL", reg1, reg2)
                self.pc += 3
            elif command == PRN:
                register = operand_a
                print(self.reg[register])
                self.pc += 2
            elif command == HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {command}")
                sys.exit(1)
