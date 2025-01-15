import tkinter as tk
from tkinter import ttk, filedialog
from instructiune import parse_file
import matplotlib.pyplot as plt


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
        self.graph_button = ttk.Button(button_frame, text="Generează Grafice", command=self.generate_graphs)
        self.graph_button.grid(row=0, column=2, padx=5)
        self.exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
        self.exit_button.grid(row=0, column=3, padx=5)

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
        instruction_list_frame = ttk.LabelFrame(root, text="Lista Instrucţiuni")
        instruction_list_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.instruction_listbox = tk.Listbox(instruction_list_frame, height=10, width=50)
        self.instruction_listbox.grid(row=0, column=0, sticky="nsew")

    def simulate_write(self, cache, address, write_policy, cache_log):
        block_index = address % len(cache)
        block = cache[block_index]

        if write_policy == "write-through":
            cache_log.write(f"Write-through: Writing to cache and memory at address {address}\n")
        elif write_policy == "write-back":
            if block["address"] is not None and block["address"] != address and block["dirty_bit"] == 1:
                cache_log.write(f"Evicting dirty block {block['address']} to memory\n")
            block["dirty_bit"] = 1
            cache_log.write(f"Write-back: Writing to cache at address {address}\n")

        block["address"] = address

    def simulate_read(self, cache, address, cache_log):
        block_index = address % len(cache)
        block = cache[block_index]

        if block["address"] == address:
            cache_log.write(f"Cache hit at address {address}\n")
        else:
            cache_log.write(f"Cache miss at address {address}\n")
            if block["dirty_bit"] == 1:
                cache_log.write(f"Evicting dirty block {block['address']} to memory\n")
            block["address"] = address
            block["dirty_bit"] = 0

    def generate_graphs(self):
        block_sizes = [4, 8, 16, 32]
        hit_rates = []
        miss_rates = []

        for block_size in block_sizes:
            hits, misses = self.simulate_for_block_size(block_size)
            total = hits + misses
            hit_rates.append(hits / total if total > 0 else 0)
            miss_rates.append(misses / total if total > 0 else 0)

        # Grafic Rata de Hit
        plt.figure()
        plt.plot(block_sizes, hit_rates, marker="o")
        plt.title("Rata de Hit în funcție de Block Size")
        plt.xlabel("Dimensiunea Blocului")
        plt.ylabel("Rata de Hit")
        plt.grid()
        plt.show()

        # Grafic Rata de Miss
        plt.figure()
        plt.plot(block_sizes, miss_rates, marker="o")
        plt.title("Rata de Miss în funcție de Block Size")
        plt.xlabel("Dimensiunea Blocului")
        plt.ylabel("Rata de Miss")
        plt.grid()
        plt.show()

    def simulate_for_block_size(self, block_size):
        # Simulare simplificată pentru dimensiuni diferite de blocuri
        hits = 0
        misses = 0
        cache = [{"address": None, "dirty_bit": 0} for _ in range(block_size)]

        for instr in self.instructions:
            address = instr.address
            block_index = address % len(cache)
            block = cache[block_index]

            if block["address"] == address:
                hits += 1
            else:
                misses += 1
                block["address"] = address
                block["dirty_bit"] = 0

        return hits, misses

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        print(f"Fişier selectat: {self.file_path}")

    def start_simulation(self):
        if not self.file_path:
            print("Niciun fişier selectat!")
            return

        self.instructions = parse_file(self.file_path)

        with open("log.txt", "w") as log_file, open("cachelog.txt", "w") as cache_log:
            log_file.write("Simulation Log:\n")
            log_file.write("=================\n")

            cache_log.write("Cache Access Log:\n")
            cache_log.write("=================\n")

            cache = [{"address": None, "dirty_bit": 0} for _ in range(16)]
            write_policy = self.write_policy_var.get()

            ticks = 0
            fetched_instructions = []

            FR = int(self.fr_combobox.get())
            IR = int(self.irmax_combobox.get())
            IBS = int(self.ibs_combobox.get())
            self.ibs = []
            executed_instructions = 0

            nr_load = 0
            nr_store = 0
            nr_branch = 0

            while self.instructions or self.ibs:
                ticks += 1
                log_file.write(f"\n--- TICK {ticks} ---\n")
                log_file.write(f"Cache size before fetch: {len(self.instructions)}\n")
                log_file.write(f"IBS size before fetch: {len(self.ibs)}\n")

                # Fetch instructions
                fetched_count = 0
                while len(self.ibs) < IBS and self.instructions:
                    for _ in range(FR):
                        if self.instructions and len(self.ibs) < IBS:
                            instr = self.instructions.pop(0)
                            self.ibs.append(instr)
                            fetched_count += 1
                            log_file.write(
                                f"Fetched: {instr.tip_instructiune}, PC: {instr.pc_curent}, Address: {instr.address}\n")

                log_file.write(f"Fetched {fetched_count} instructions into IBS. IBS size: {len(self.ibs)}\n")

                # Execute instructions
                executed_count = 0
                for _ in range(IR):
                    if self.ibs:
                        instr = self.ibs.pop(0)
                        executed_count += 1
                        executed_instructions += 1
                        log_file.write(
                            f"Executed: {instr.tip_instructiune}, PC: {instr.pc_curent}, Address: {instr.address}\n")

                        if instr.tip_instructiune == 'L':
                            nr_load += 1
                            self.simulate_read(cache, instr.address, cache_log)
                        elif instr.tip_instructiune == 'S':
                            nr_store += 1
                            self.simulate_write(cache, instr.address, write_policy, cache_log)
                        elif instr.tip_instructiune in ['BS', 'BM', 'BT', 'NT', 'B']:
                            nr_branch += 1

                log_file.write(
                    f"Executed {executed_count} instructions from IBS. IBS size after execution: {len(self.ibs)}\n")

            # Calculate issue rate
            issue_rate = executed_instructions / ticks if ticks > 0 else 0
            log_file.write(f"\nExecution completed in {ticks} ticks.\n")
            log_file.write(f"Total executed instructions: {executed_instructions}\n")
            log_file.write(f"Issue Rate: {issue_rate:.2f}\n")

            print(f"\nExecution completed in {ticks} cycles.")
            print(f"Issue Rate: {issue_rate:.2f}")

            # Update UI fields
            self.ticks_entry.delete(0, tk.END)
            self.ticks_entry.insert(0, str(ticks))

            self.load_entry.delete(0, tk.END)
            self.load_entry.insert(0, str(nr_load))

            self.store_entry.delete(0, tk.END)
            self.store_entry.insert(0, str(nr_store))

            self.branch_entry.delete(0, tk.END)
            self.branch_entry.insert(0, str(nr_branch))

            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, str(executed_instructions))

            self.issue_rate_entry.delete(0, tk.END)
            self.issue_rate_entry.insert(0, f"{issue_rate:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CacheSimulatorApp(root)
    root.mainloop()
