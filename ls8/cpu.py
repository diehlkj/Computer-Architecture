"""CPU functionality."""

import sys

# * -V- CPU Instructions --------------------------------
HLT = 0b00000001    # * Stop Code

# * -V- 2 Args: [Register Index | Value to Store] -- Stores a Value in Specified Register Index
LDI = 0b10000010

# * -V- 1 Arg: [Register Index] -- Prints a Value From Register
PRN = 0b01000111

# * Arithmatic Operations --------------------------------
# * -V- 2 Args: [reg_a | reg_b] -- Triggers the ALU to add and return the result
ADD = 0b10100000
# * -V- 2 Args: [reg_a | reg_b] -- Triggers the ALU to subtract and return the result
SUB = 0b10100001
# * -V- 2 Args: [reg_a | reg_b] -- Triggers the ALU to multiply and return the result
MUL = 0b10100010
# * -V- 2 Args: [reg_a | reg_b] -- Triggers the ALU to divide and return the result
DIV = 0b10100011
# * -V- 2 Args: [reg_a | reg_b] -- Triggers the ALU to mod and return the result
MOD = 0b10100100

# * Stack Operations --------------------------------
# * -V- 1 Arg: [Register Index] -- Pushes value stored at Arg into memory at location of Stack Pointer
PUSH = 0b01000101
# * -V- 1 Arg: [Register Index] -- Copys value at stack pointer to Arg
POP = 0b01000110

# * Call/Return Operations --------------------------------
# * -V- 1 Arg: [Register Index] -- Pushes value stored at Arg into memory at location of Stack Pointer
CALL = 0b01010000
# * -V- 0 Args
RET = 0b00010001

# ? Sprint Challenge Operations - Lable After Completion
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8     # * 8 bytes of registers
        self.ram = [0] * 256        # * 256 bytes of memory
        # * Program Counter: Index in the memory array of currently executing instruction
        self.pc = 0
        self.fl = 0b00000000

    def load(self):
        """Load a program into memory."""

        address = 0

        program = sys.argv[1]

        for line in open(f"examples/{program}", "r"):
            if not line.startswith("#") and line.strip():

                instruction = line.strip().split(" ")

                # ! print(f"Instruction: {instruction[0]} | At Address: {address}")

                # * the '2' in int() tells it to be base 2. This keeps leading 0s
                self.ram[address] = int(instruction[0], 2)

                # ! print(f"Memorey at address {address} is {self.ram[address]} and is type: {type(self.ram[address])} \n")
                address += 1

    # * Memory Methods (read/write)
        # * MAR (Memory Address Register)
            # * Address being read or written to

        # * MDR (Memory Data Register)
            # * Data being read or written

    def ram_read(self, MAR):
        # * Returns the value stored at requested memory address
        MDR = self.ram[MAR]

        return MDR

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    # * Arithmetic Logic Unit

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # ! print(f"Ran {op} in ALU - reg_a: {reg_a} | reg_b: {reg_b}")

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]

        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]

        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]

        elif op == "MOD":
            self.register[reg_a] %= self.register[reg_b]
            
        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.fl = 0b00000001
            else:
                self.fl = 0b00000000

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
        # ? Spec Refrences:
        # ? Instruction Layout:     Line 152
        # ? LDI:                    Line 444
        # ? PRN:                    Line 559
        # ? CALL:                   Line 211
        # ? RET:                    Line 590
        # * Flags:                  Line 25
        # ? CMP:                    Line 227
        # ? JMP:                    Line 403
        # ? JEQ:                    Line 341
        # ? JNE:                    Line 417
        
        # * The register is made up of 8 bits. If a particular bit is set, that flag is "true".

        # * `FL` bits: `00000LGE`

        # * `L` Less-than: during a `CMP`, set to 1 if registerA is less than registerB,
        # * zero otherwise.
        # * `G` Greater-than: during a `CMP`, set to 1 if registerA is greater than
        # * registerB, zero otherwise.
        # * `E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero
        # * otherwise.

        self.pc = 0                 # * Start program counter at 0
        self.register[7] = 0xf3     # * Set stack pointer to starting address
        running = True              # * Start running the CPU

        while running:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                # ! print(f"Ran LDI: {operand_b} assigned to {operand_a}")
                # ? Takes 2 args: first is register, second is value
                self.register[operand_a] = operand_b
                self.pc += 2

            elif IR == PRN:
                print_value = self.register[operand_a]
                print(print_value)
                self.pc += 1

        # * ALU Mathematic Instructions --------------------------------
            elif IR == ADD:
                # ! print("Ran MUL")
                # ? Takes 2 args: first is register a, second is register aregister b
                self.alu("ADD", operand_a, operand_b)

                self.pc += 2

            elif IR == SUB:
                # ! print("Ran MUL")
                # ? Takes 2 args: first is register a, second is register aregister b
                self.alu("SUB", operand_a, operand_b)

                self.pc += 2

            elif IR == MUL:
                # ! print("Ran MUL")
                # ? Takes 2 args: first is register a, second is register aregister b
                self.alu("MUL", operand_a, operand_b)

                self.pc += 2

            elif IR == DIV:
                # ! print("Ran MUL")
                # ? Takes 2 args: first is register a, second is register aregister b
                self.alu("DIV", operand_a, operand_b)

                self.pc += 2

            elif IR == MOD:
                # ! print("Ran MUL")
                # ? Takes 2 args: first is register a, second is register aregister b
                self.alu("MOD", operand_a, operand_b)

                self.pc += 2

        # * Stack Instructions --------------------------------
            elif IR == PUSH:
                # ! print("Ran PUSH")
                # ? Takes 1 args: register address of value to push

                self.register[7] -= 1  # * Move SP down
                # * Puts value of Rn to memory location of SP
                self.ram[self.register[7]] = self.register[operand_a]

                self.pc += 1

            elif IR == POP:
                # ! print("Ran POP")
                # ? Takes 1 args: register address to copy popped value to

                # * Puts value of Rn to memory location of SP
                self.register[operand_a] = self.ram[self.register[7]]
                self.register[7] += 1  # * Move SP up

                self.pc += 1
                
            elif IR == CALL:
                # ! print(f"Ran CALL | PC: {self.pc} | + 2 {self.pc + 2}")
                self.register[7] -= 1
                self.ram[self.register[7]] = self.pc + 2
                
                # ? Set pc to location of function
                self.pc = self.register[operand_a]
                
                self.pc -= 1 # * pc - 1 to offset the difference from outside if-tree pc inc
                
                
            elif IR == RET:
                # ! print("Ran RET")
                # ? pops the program counter position from the stack and returns the pc to it
                self.pc = self.ram[self.register[7]]
                self.register[7] += 1  # * Move SP up
                
        # * Comparison Instructions --------------------------------
            elif IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 2
            
            elif IR == JMP:
                # ? Jumps to given address
                self.pc = self.register[operand_a] - 1
                
            elif IR == JEQ:
                # ? Jumps to given address if flag E is true
                if self.fl == 0b00000001:
                    self.pc = self.register[operand_a] - 1
                else:
                    self.pc += 1
                
            elif IR == JNE:
                # ? Jumps to given address if flag E is false
                if self.fl == 0b00000000:
                    self.pc = self.register[operand_a] - 1
                else:
                    self.pc += 1
                

        # * Halt the CPU --------------------------------
            elif IR == HLT:
                running = False

            self.pc += 1
