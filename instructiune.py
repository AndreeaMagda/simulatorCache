class Instructiune:
    def __init__(self, tip_instructiune, pc_curent, address):
        self.tip_instructiune = tip_instructiune
        self.pc_curent = pc_curent
        self.address = address

def parse_file(file_path):
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                tip = parts[0]
                pc = int(parts[1])
                address = int(parts[2])
                instructions.append(Instructiune(tip, pc, address))
    return instructions
