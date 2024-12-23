import sys
import struct
import xml.etree.ElementTree as ET


class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.instructions = []

    def assemble(self):
        """Читает исходный код, преобразует в бинарный формат и создает лог."""
        with open(self.input_file, "r") as file:
            lines = file.readlines()

        binary_data = bytearray()
        root = ET.Element("log")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):  # Пропускаем пустые строки и комментарии
                continue

            parts = line.split()
            command = parts[0]
            args = list(map(int, parts[1:]))

            if command == "LOAD_CONST":
                # Формат команды: A=8, B=константа
                opcode = 0xC8
                const = args[0]
                binary_data.extend(struct.pack(">BI", opcode, const))
                self.instructions.append({"command": "LOAD_CONST", "opcode": opcode, "const": const})

            elif command == "LOAD_MEM":
                # Формат команды: A=14, B=смещение
                opcode = 0xAE
                offset = args[0]
                binary_data.extend(struct.pack(">BH", opcode, offset))
                self.instructions.append({"command": "LOAD_MEM", "opcode": opcode, "offset": offset})

            elif command == "STORE_MEM":
                # Формат команды: A=15, B=адрес
                opcode = 0xEF
                address = args[0]
                binary_data.extend(struct.pack(">BI", opcode, address))
                self.instructions.append({"command": "STORE_MEM", "opcode": opcode, "address": address})

            elif command == "BITSHIFT_LEFT":
                # Формат команды: A=9, B=адрес
                opcode = 0x79
                address = args[0]
                binary_data.extend(struct.pack(">BI", opcode, address))
                self.instructions.append({"command": "BITSHIFT_LEFT", "opcode": opcode, "address": address})

        # Сохраняем бинарный файл
        with open(self.output_file, "wb") as bin_file:
            bin_file.write(binary_data)

        # Создаем XML-лог
        for instr in self.instructions:
            instr_elem = ET.SubElement(root, "instruction")
            for key, value in instr.items():
                ET.SubElement(instr_elem, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(self.log_file, encoding="unicode")

        print(f"Ассемблирование завершено. Бинарный файл: {self.output_file}, Лог: {self.log_file}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python assembler.py <input_file> <output_file> <log_file>")
        sys.exit(1)

    assembler = Assembler(sys.argv[1], sys.argv[2], sys.argv[3])
    assembler.assemble()