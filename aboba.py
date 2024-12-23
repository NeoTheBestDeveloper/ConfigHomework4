import sys
import struct
import xml.etree.ElementTree as ET


class Interpreter:
    def __init__(self, binary_file, memory_range, result_file):
        self.binary_file = binary_file
        self.memory_range = memory_range
        self.result_file = result_file
        self.memory = [0] * 1024  # Простая модель памяти
        self.accumulator = 0

    def execute(self):
        """Выполняет команды из бинарного файла."""
        with open(self.binary_file, "rb") as file:
            binary_data = file.read()

        pc = 0  # Программный счетчик
        while pc < len(binary_data):
            opcode = binary_data[pc]
            if opcode == 0xC8:  # LOAD_CONST
                _, const = struct.unpack(">BI", binary_data[pc:pc + 5])
                self.accumulator = const
                pc += 5

            elif opcode == 0xAE:  # LOAD_MEM
                _, offset = struct.unpack(">BH", binary_data[pc:pc + 3])
                address = self.accumulator + offset
                self.accumulator = self.memory[address]
                pc += 3

            elif opcode == 0xEF:  # STORE_MEM
                _, address = struct.unpack(">BI", binary_data[pc:pc + 5])
                self.memory[address] = self.accumulator
                pc += 5

            elif opcode == 0x79:  # BITSHIFT_LEFT
                _, address = struct.unpack(">BI", binary_data[pc:pc + 5])
                self.memory[address] = self.memory[address] << self.accumulator
                pc += 5

        # Сохраняем результат в XML
        root = ET.Element("memory")
        start, end = self.memory_range
        for i in range(start, end + 1):
            mem_elem = ET.SubElement(root, "cell")
            mem_elem.set("address", str(i))
            mem_elem.text = str(self.memory[i])

        tree = ET.ElementTree(root)
        tree.write(self.result_file, encoding="unicode")

        print(f"Выполнение завершено. Результат сохранен в {self.result_file}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python interpreter.py <binary_file> <memory_start> <memory_end> <result_file>")
        sys.exit(1)

    binary_file = sys.argv[1]
    memory_start = int(sys.argv[2])
    memory_end = int(sys.argv[3])
    result_file = sys.argv[4]

    interpreter = Interpreter(binary_file, (memory_start, memory_end), result_file)
    interpreter.execute()