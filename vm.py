import os

class VirtualMachine:
    def __init__(self):
        self.AC = 0
        self.PC = 0
        self.memory = {}
        self.program = []
        self.running = False

    def reset(self):
        self.AC = 0
        self.memory = {}
        self.program = []
        self.PC = 0
        self.running = False

    def load_program(self, instructions):
        self.program = instructions

    def execute_instruction(self, instruction):
        parts = instruction.split()
        if len(parts) == 0:
            return
        opcode = parts[0].upper()
        try:
            operand = int(parts[1]) if len(parts) > 1 else None
        except ValueError:
            operand = None

        if opcode == "CONST":
            self.AC = operand
        elif opcode == "LOAD":
            self.AC = self.memory.get(operand, 0)
        elif opcode == "STORE":
            self.memory[operand] = self.AC
        elif opcode == "ADD":
            self.AC += self.memory.get(operand, 0)
        elif opcode == "SUB":
            self.AC -= self.memory.get(operand, 0)
        elif opcode == "MUL":
            self.AC *= self.memory.get(operand, 0)
        elif opcode == "DIV":
            try:
                self.AC //= self.memory.get(operand, 0)
            except ZeroDivisionError:
                print("Error: Division by zero")
                self.running = False
        elif opcode == "MOD":
            try:
                self.AC %= self.memory.get(operand, 0)
            except ZeroDivisionError:
                print("Error: Modulo by zero")
                self.running = False
        elif opcode == "CLR":
            self.AC = 0
        elif opcode == "JMP":
            self.PC = operand - 1
        elif opcode == "JNEG":
            if self.AC < 0:
                self.PC = operand - 1
        elif opcode == "JZERO":
            if self.AC == 0:
                self.PC = operand - 1
        elif opcode == "HALT":
            self.running = False
        else:
            print(f"Unknown instruction: {opcode}")

    def run(self):
        self.running = True
        while self.running and self.PC < len(self.program):
            instruction = self.program[self.PC]
            self.execute_instruction(instruction)
            self.PC += 1

    def repl(self):
        print("Simple Virtual Machine REPL. Type '%help' for commands.")
        while True:
            command = input(">>> ").strip()
            if command == "%exit":
                break
            elif command == "%help":
                print("Commands:")
                print("  %open [file] - Adds instruction from file to the program")
                print("  %list - List the current program")
                print("  %run - Run the program")
                print("  %reset - Reset the virtual machine")
                print("  %exit - Exit the REPL")
            elif command.startswith("%open "):
                filename = command[5:].strip()
                try:
                    with open(filename, "r") as file:
                        instructions = file.readlines()
                        self.load_program([line.strip() for line in instructions])
                    print(f"Loaded program from {filename}")
                except FileNotFoundError:
                    print(f"File {filename} not found.")
            elif command == "%list":
                for i, instr in enumerate(self.program):
                    print(f"{i + 1}: {instr}")
            elif command == "%run":
                self.PC = 0
                self.run()
                print("  AC: ", self.AC)
                print("  Memory:", self.memory)
            elif command == "%reset":
                self.reset()
                print("Virtual machine reset.")
            elif command == "%clear":
                os.system("cls" if os.name == "nt" else "clear")
            elif command.startswith("%"):
                print("Unknown command. Type 'help' for a list of commands.")
            else:
                self.program.append(command)

if __name__ == "__main__" :
    vm = VirtualMachine()
    vm.repl()