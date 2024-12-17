import tkinter as tk
from tkinter import ttk, filedialog
from instructiune import parse_file



class CacheSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Cache")
        self.create_interface()

    def create_interface(self):
        # Parametri Simulator
        parameters_frame = ttk.LabelFrame(root, text="Parametri Simulator")
        parameters_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(parameters_frame, text="Fetch Rate (FR):").grid(row=0, column=0, sticky="w")
        self.fr_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.fr_combobox.grid(row=0, column=1)
        self.fr_combobox.set(4)

        ttk.Label(parameters_frame, text="Issue Rate Maxim (IRmax):").grid(row=1, column=0, sticky="w")
        self.irmax_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4])
        self.irmax_combobox.grid(row=1, column=1)
        self.irmax_combobox.set(2)

        ttk.Label(parameters_frame, text="Instruction Buffer Size (IBS):").grid(row=2, column=0, sticky="w")
        self.ibs_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.ibs_combobox.grid(row=2, column=1)
        self.ibs_combobox.set(4)

        ttk.Label(parameters_frame, text="Latenta (for hit in cache):").grid(row=3, column=0, sticky="w")
        self.latency_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 5, 10])
        self.latency_combobox.grid(row=3, column=1)
        self.latency_combobox.set(1)

        ttk.Label(parameters_frame, text="N_PEN (miss in cache):").grid(row=4, column=0, sticky="w")
        self.n_pen_combobox = ttk.Combobox(parameters_frame, values=[5, 10, 15, 20])
        self.n_pen_combobox.grid(row=4, column=1)
        self.n_pen_combobox.set(10)

        ttk.Label(parameters_frame, text="Nr. Set Regiştri:").grid(row=5, column=0, sticky="w")
        self.reg_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.reg_combobox.grid(row=5, column=1)
        self.reg_combobox.set(2)

        # Parametri Cache
        cache_frame = ttk.LabelFrame(root, text="Parametri Cache (Mapare Directa)")
        cache_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(cache_frame, text="Instruction Cache").grid(row=0, column=0, sticky="w")
        ttk.Label(cache_frame, text="Block Size:").grid(row=1, column=0, sticky="w")
        self.ic_block_combobox = ttk.Combobox(cache_frame, values=[4, 8, 16, 32])
        self.ic_block_combobox.grid(row=1, column=1)
        self.ic_block_combobox.set(4)

        # Instrucţiuni
        instructions_frame = ttk.LabelFrame(root, text="Instrucţiuni")
        instructions_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(instructions_frame, text="Load:").grid(row=0, column=0, sticky="w")
        self.load_entry = ttk.Entry(instructions_frame)
        self.load_entry.grid(row=0, column=1)

        ttk.Label(instructions_frame, text="Store:").grid(row=1, column=0, sticky="w")
        self.store_entry = ttk.Entry(instructions_frame)
        self.store_entry.grid(row=1, column=1)

        ttk.Label(instructions_frame, text="Branch:").grid(row=2, column=0, sticky="w")
        self.branch_entry = ttk.Entry(instructions_frame)
        self.branch_entry.grid(row=2, column=1)

        ttk.Label(instructions_frame, text="Total:").grid(row=3, column=0, sticky="w")
        self.total_entry = ttk.Entry(instructions_frame)
        self.total_entry.grid(row=3, column=1)

        # Rezultate
        results_frame = ttk.LabelFrame(root, text="Rezultate")
        results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(results_frame, text="One-Cycle:").grid(row=0, column=0, sticky="w")
        self.one_cycle_entry = ttk.Entry(results_frame)
        self.one_cycle_entry.grid(row=0, column=1)

        ttk.Label(results_frame, text="Issue Rate:").grid(row=1, column=0, sticky="w")
        self.issue_rate_entry = ttk.Entry(results_frame)
        self.issue_rate_entry.grid(row=1, column=1)

        ttk.Label(results_frame, text="Ticks:").grid(row=2, column=0, sticky="w")
        self.ticks_entry = ttk.Entry(results_frame)
        self.ticks_entry.grid(row=2, column=1)

        # Buttons
        button_frame = ttk.Frame(root)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        self.file_button = ttk.Button(button_frame, text="Alege fişier", command=self.choose_file)
        self.file_button.grid(row=0, column=0, padx=5)
        self.start_button = ttk.Button(button_frame, text="Start Simulare", command=self.start_simulation)
        self.start_button.grid(row=0, column=1, padx=5)
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=0, column=2, padx=5)

        self.file_path = None

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        print(f"Fişier selectat: {self.file_path}")

    def start_simulation(self):
        if not self.file_path:
            print("Niciun fişier selectat!")
            return

        # Citire parametri din interfață
        n_pen = int(self.n_pen_combobox.get())
        block_size = int(self.ic_block_combobox.get())


        instructions = parse_file(self.file_path)

        load_count = sum(1 for instr in instructions if instr.tip_instructiune == 'L')
        store_count = sum(1 for instr in instructions if instr.tip_instructiune == 'S')
        branch_count = sum(1 for instr in instructions if instr.tip_instructiune in ['BS', 'BM', 'BT', 'NT'])

        total_count = len(instructions)

        self.load_entry.delete(0, tk.END)
        self.load_entry.insert(0, str(load_count))
        self.store_entry.delete(0, tk.END)
        self.store_entry.insert(0, str(store_count))
        self.branch_entry.delete(0, tk.END)
        self.branch_entry.insert(0, str(branch_count))
        self.total_entry.delete(0, tk.END)
        self.total_entry.insert(0, str(total_count))





if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorApp(root)
    root.mainloop()
