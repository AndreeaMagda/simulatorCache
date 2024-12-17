class Instructiune:
    def __init__(self, tip_instructiune, pc_curent, target):
        self.tip_instructiune = tip_instructiune
        self.pc_curent = pc_curent
        self.target = target

def parse_file(file_path):
    instructions = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 3:
                tip = parts[0]
                pc = int(parts[1])
                target = int(parts[2])
                instructions.append(Instructiune(tip, pc, target))
    return instructions


