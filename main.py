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

        # Write Policy Selection
        ttk.Label(parameters_frame, text="Write Policy:").grid(row=3, column=0, sticky="w")
        self.write_policy_var = tk.StringVar(value="write-through")  # Default is write-through
        self.write_through_radio = ttk.Radiobutton(
            parameters_frame, text="Write-Through", variable=self.write_policy_var, value="write-through"
        )
        self.write_through_radio.grid(row=3, column=1, sticky="w")
        self.write_back_radio = ttk.Radiobutton(
            parameters_frame, text="Write-Back", variable=self.write_policy_var, value="write-back"
        )
        self.write_back_radio.grid(row=3, column=2, sticky="w")

        # Lista  de instrucțiuni
        instruction_list_frame = ttk.LabelFrame(root, text="Lista Instrucțiuni")
        instruction_list_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.instruction_listbox = tk.Listbox(instruction_list_frame, height=10, width=50)
        self.instruction_listbox.grid(row=0, column=0, sticky="nsew")


    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        print(f"Fişier selectat: {self.file_path}")

    def start_simulation(self):
        if not self.file_path:
            print("Niciun fişier selectat!")
            return

        self.cache = parse_file(self.file_path)
        self.ibs = []

        FR = int(self.fr_combobox.get())
        IR = int(self.irmax_combobox.get())
        IBS = int(self.ibs_combobox.get())
        self.process_instructions(FR, IR, IBS)

        TICKS = 0
        nrInstrProcesate = 0
        nrBranchProcesate = 0
        nrStoreProcesate = 0
        nrLoadProcesate = 0

        self.instructions = parse_file(self.file_path)
        self.instruction_listbox.delete(0, tk.END)

        for instr in self.instructions:
            display_text = f"{instr.tip_instructiune} - PC: {instr.pc_curent}, Address: {instr.address}"
            self.instruction_listbox.insert(tk.END, display_text)

        nrInstrProcesate = len(self.instructions)
        nrBranchProcesate = sum(
            1 for instr in self.instructions if instr.tip_instructiune in ['BS', 'BM', 'BT', 'NT', 'BR'])
        nrStoreProcesate = sum(1 for instr in self.instructions if instr.tip_instructiune == 'S')
        nrLoadProcesate = sum(1 for instr in self.instructions if instr.tip_instructiune == 'L')

        for instr in self.instructions:
            if instr.tip_instructiune in ['BS', 'BM', 'BT', 'NT', 'BR']:
                TICKS += 1
            elif instr.tip_instructiune in ['S', 'L']:
                TICKS += 1

        self.ticks_entry.delete(0, tk.END)
        self.ticks_entry.insert(0, str(TICKS))

        self.load_entry.delete(0, tk.END)
        self.load_entry.insert(0, str(nrLoadProcesate))

        self.store_entry.delete(0, tk.END)
        self.store_entry.insert(0, str(nrStoreProcesate))

        self.branch_entry.delete(0, tk.END)
        self.branch_entry.insert(0, str(nrBranchProcesate))

        self.total_entry.delete(0, tk.END)
        self.total_entry.insert(0, str(nrInstrProcesate))

    def process_instructions(self, FR, IR, IBS):
        TICKS = 0
        executed_instructions = 0  

        with open("log.txt", "w") as log_file:
            log_file.write("Simulation Log:\n")
            log_file.write("=================\n")

            while self.cache or self.ibs:
                log_file.write(f"\n--- TICK {TICKS + 1} ---\n")
                log_file.write(f"Cache size before fetch: {len(self.cache)}\n")
                log_file.write(f"IBS size before fetch: {len(self.ibs)}\n")

                print(f"\n--- TICK {TICKS + 1} ---")
                print(f"Cache size before fetch: {len(self.cache)}")
                print(f"IBS size before fetch: {len(self.ibs)}")

                # Fetch instrucțiuni
                fetched_count = 0
                while len(self.ibs) < IBS and self.cache:
                    for _ in range(FR):
                        if self.cache and len(self.ibs) < IBS:
                            instr = self.cache.pop(0)
                            self.ibs.append(instr)
                            fetched_count += 1
                            log_file.write(
                                f"Fetched: {instr.tip_instructiune}, PC: {instr.pc_curent}, Address: {instr.address}\n")

                log_file.write(f"Fetched {fetched_count} instructions into IBS. IBS size: {len(self.ibs)}\n")

                # Execute instrucțiuni
                executed_count = 0
                for _ in range(IR):
                    if self.ibs:
                        instr = self.ibs.pop(0)
                        executed_count += 1
                        executed_instructions += 1
                        print(f"Executed: {instr.tip_instructiune}, PC: {instr.pc_curent}, Address: {instr.address}")
                        log_file.write(
                            f"Executed: {instr.tip_instructiune}, PC: {instr.pc_curent}, Address: {instr.address}\n")

                log_file.write(
                    f"Executed {executed_count} instructions from IBS. IBS size after execution: {len(self.ibs)}\n")

                TICKS += 1


            issue_rate = executed_instructions / TICKS if TICKS > 0 else 0
            log_file.write(f"\nExecution completed in {TICKS} cycles.\n")
            log_file.write(f"Total executed instructions: {executed_instructions}\n")
            log_file.write(f"Issue Rate: {issue_rate:.2f}\n")


            self.issue_rate_entry.delete(0, tk.END)
            self.issue_rate_entry.insert(0, f"{issue_rate:.2f}")

        print(f"\nExecution completed in {TICKS} cycles.")
        print(f"Issue Rate: {issue_rate:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorApp(root)
    root.mainloop()
