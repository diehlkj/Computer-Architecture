"""CPU functionality."""

import sys

# * CPU Instructions
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8     # * 8 bytes of registers
        self.ram = [0] * 256        # * 256 bytes of memory
        self.pc = 0                 # * Program Counter: Index in the memory array of currently executing instruction

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
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
            # ?

        self.pc = 0
        
        running = True
        
        while running:
            
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if IR == LDI:
                # ? Takes 2 args: first is register, second is value
                self.register[operand_a] = operand_b
                self.pc += 2
                
            if IR == PRN:
                print_value = self.register[operand_a]
                print(print_value)
                self.pc += 1
                
            elif IR == HLT:
                running = False
            
            self.pc += 1 
