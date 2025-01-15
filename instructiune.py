class Instruction:
    def __init__(self, tip_instructiune, pc_curent, address):
        self.tip_instructiune = tip_instructiune
        self.pc_curent = int(pc_curent)
        self.address = int(address)

def parse_file(file_path):
    instructions = []
    with open(file_path, "r") as file:
        for line in file:
            # Încearcă să desparți datele pe spații
            parts = line.split()
            if len(parts) >= 3:  # Asigură-te că ai minim 3 coloane
                tip_instructiune = parts[0]  # Primul element
                pc_curent = parts[1]  # Al doilea element
                address = parts[2]  # Al treilea element
                # Creează un obiect de tip Instruction
                instructions.append(Instruction(tip_instructiune, pc_curent, address))
    return instructions

