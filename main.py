import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class CacheSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulator Cache")

        # Parameters Panel
        parameters_frame = ttk.LabelFrame(root, text="Parametri Simulator")
        parameters_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(parameters_frame, text="Fetch Rate (FR):").grid(row=0, column=0, sticky="w")
        self.fr_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.fr_combobox.grid(row=0, column=1, sticky="w")

        ttk.Label(parameters_frame, text="Issue Rate Maxim (IRmax):").grid(row=1, column=0, sticky="w")
        self.irmax_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4])
        self.irmax_combobox.grid(row=1, column=1, sticky="w")

        ttk.Label(parameters_frame, text="Instruction Buffer Size (IBS):").grid(row=2, column=0, sticky="w")
        self.ibs_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.ibs_combobox.grid(row=2, column=1, sticky="w")

        ttk.Label(parameters_frame, text="Latenta (for hit in cache):").grid(row=3, column=0, sticky="w")
        self.latency_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 5, 10])
        self.latency_combobox.grid(row=3, column=1, sticky="w")

        ttk.Label(parameters_frame, text="N_PEN (miss in cache):").grid(row=4, column=0, sticky="w")
        self.n_pen_combobox = ttk.Combobox(parameters_frame, values=[5, 10, 15, 20])
        self.n_pen_combobox.grid(row=4, column=1, sticky="w")

        ttk.Label(parameters_frame, text="Nr. Set Regiştri:").grid(row=5, column=0, sticky="w")
        self.reg_combobox = ttk.Combobox(parameters_frame, values=[1, 2, 4, 8])
        self.reg_combobox.grid(row=5, column=1, sticky="w")

        # Cache Parameters Panel
        cache_frame = ttk.LabelFrame(root, text="Parametri Cache (Mapare Directa)")
        cache_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(cache_frame, text="Instruction Cache Block Size:").grid(row=0, column=0, sticky="w")
        self.ic_block_combobox = ttk.Combobox(cache_frame, values=[4, 8, 16, 32])
        self.ic_block_combobox.grid(row=0, column=1, sticky="w")

        ttk.Label(cache_frame, text="Size_IC:").grid(row=1, column=0, sticky="w")
        self.size_ic_combobox = ttk.Combobox(cache_frame, values=[32, 64, 128])
        self.size_ic_combobox.grid(row=1, column=1, sticky="w")

        ttk.Label(cache_frame, text="Data Cache Block Size:").grid(row=2, column=0, sticky="w")
        self.dc_block_combobox = ttk.Combobox(cache_frame, values=[4, 8, 16, 32])
        self.dc_block_combobox.grid(row=2, column=1, sticky="w")

        ttk.Label(cache_frame, text="Size_DC:").grid(row=3, column=0, sticky="w")
        self.size_dc_combobox = ttk.Combobox(cache_frame, values=[32, 64, 128])
        self.size_dc_combobox.grid(row=3, column=1, sticky="w")

        # Unimport/Biport Options
        self.unimport_radio = ttk.Radiobutton(cache_frame, text="Uniport", value=1)
        self.unimport_radio.grid(row=4, column=0, sticky="w")
        self.biport_radio = ttk.Radiobutton(cache_frame, text="Biport", value=2)
        self.biport_radio.grid(row=4, column=1, sticky="w")

        # Instructions Panel
        instructions_frame = ttk.LabelFrame(root, text="Instrucţiuni")
        instructions_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(instructions_frame, text="Load:").grid(row=0, column=0, sticky="w")
        self.load_entry = ttk.Entry(instructions_frame)
        self.load_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(instructions_frame, text="Store:").grid(row=1, column=0, sticky="w")
        self.store_entry = ttk.Entry(instructions_frame)
        self.store_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(instructions_frame, text="Branch:").grid(row=2, column=0, sticky="w")
        self.branch_entry = ttk.Entry(instructions_frame)
        self.branch_entry.grid(row=2, column=1, sticky="w")

        ttk.Label(instructions_frame, text="Total:").grid(row=3, column=0, sticky="w")
        self.total_entry = ttk.Entry(instructions_frame)
        self.total_entry.grid(row=3, column=1, sticky="w")

        # Results Panel
        results_frame = ttk.LabelFrame(root, text="Rezultate")
        results_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(results_frame, text="One-Cycle:").grid(row=0, column=0, sticky="w")
        self.one_cycle_entry = ttk.Entry(results_frame)
        self.one_cycle_entry.grid(row=0, column=1, sticky="w")

        ttk.Label(results_frame, text="Issue Rate:").grid(row=1, column=0, sticky="w")
        self.issue_rate_entry = ttk.Entry(results_frame)
        self.issue_rate_entry.grid(row=1, column=1, sticky="w")

        ttk.Label(results_frame, text="Ticks:").grid(row=2, column=0, sticky="w")
        self.ticks_entry = ttk.Entry(results_frame)
        self.ticks_entry.grid(row=2, column=1, sticky="w")

        # File Selection and Simulation Start
        file_frame = ttk.Frame(root)
        file_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        self.file_button = ttk.Button(file_frame, text="Alege fişier", command=self.choose_file)
        self.file_button.grid(row=0, column=0, padx=5)

        self.start_button = ttk.Button(file_frame, text="Start Simulare", command=self.start_simulation)
        self.start_button.grid(row=0, column=1, padx=5)

        self.exit_button = ttk.Button(file_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=0, column=2, padx=5)

    def choose_file(self):
        file_path = filedialog.askopenfilename()
        print(f"File selected: {file_path}")

    def start_simulation(self):
        print("Simulation started...")

if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorApp(root)
    root.mainloop()
