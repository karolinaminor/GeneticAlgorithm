import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Import your code ---
# Make sure genetic_algorithm.py and benchmark_functions.py
# are in the same folder as this script.
try:
    from genetic_algorithm import GeneticAlgorithm
    import benchmark_functions as bf
except ImportError:
    messagebox.showerror(
        "Import Error",
        "Could not find 'genetic_algorithm.py' or 'benchmark_functions.py'. "
        "Make sure they are in the same directory as this GUI script."
    )
    exit()

class GeneticAlgorithmGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genetic Algorithm Runner")
        self.geometry("450x600")

        # --- This dictionary holds all the benchmark functions ---
        # !!! IMPORTANT !!!
        # Update this dictionary with the actual functions available
        # in your 'benchmark_functions.py' file.
        # The key is the name you want to see in the dropdown.
        # The value is the actual class or function from your module.
        self.benchmark_functions = {
            "McCormick": bf.McCormick,
            #"Ackley": bf.Ackley,       # Example: assuming you have this
            #"Rastrigin": bf.Rastrigin, # Example: assuming you have this
            #"Sphere": bf.Sphere        # Example: assuming you have this
            # Add more functions here as 'Name': bf.FunctionName
        }

        # --- This dictionary holds the GUI widgets ---
        self.widgets = {}

        # Create a main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Create the GUI elements ---
        row_index = 0

        # Benchmark Function
        self.widgets['benchmark'] = self._create_combo(
            main_frame, "Benchmark Function:",
            list(self.benchmark_functions.keys()), "McCormick", row_index
        )
        row_index += 1

        # Epochs
        self.widgets['epochs'] = self._create_entry(
            main_frame, "Epochs:", 125, row_index
        )
        row_index += 1
        
        # --- Config Parameters ---
        self.widgets['population_size'] = self._create_entry(
            main_frame, "Population Size:", 10, row_index
        )
        row_index += 1
        
        self.widgets['n_variables'] = self._create_entry(
            main_frame, "Number of Variables:", 2, row_index
        )
        row_index += 1

        # Simplified bounds: Apply same bounds to all variables
        self.widgets['bound_min'] = self._create_entry(
            main_frame, "Min Bound (for all):", -3, row_index
        )
        row_index += 1
        self.widgets['bound_max'] = self._create_entry(
            main_frame, "Max Bound (for all):", 4, row_index
        )
        row_index += 1
        
        self.widgets['precision'] = self._create_entry(
            main_frame, "Precision:", 3, row_index
        )
        row_index += 1
        
        self.widgets['p_mutation'] = self._create_entry(
            main_frame, "P(mutation):", 0.09, row_index
        )
        row_index += 1

        self.widgets['p_inversion'] = self._create_entry(
            main_frame, "P(inversion):", 0.09, row_index
        )
        row_index += 1
        
        self.widgets['elite_p'] = self._create_entry(
            main_frame, "Elite Percentage:", 0.15, row_index
        )
        row_index += 1

        # --- Crossover Method ---
        # !!! IMPORTANT !!!
        # Update this list with the crossover methods your code accepts
        crossover_options = ['one_point', 'two_point', 'uniform']
        self.widgets['crossover_method'] = self._create_combo(
            main_frame, "Crossover Method:", crossover_options, 'two_point', row_index
        )
        row_index += 1

        # --- Mutation Method ---
        # !!! IMPORTANT !!!
        # Update this list with the mutation methods your code accepts
        mutation_options = ['one_point', 'multiple_point']
        self.widgets['mutation_method'] = self._create_combo(
            main_frame, "Mutation Method:", mutation_options, 'one_point', row_index
        )
        row_index += 1

        # --- Optimization ---
        self.widgets['optimization'] = self._create_combo(
            main_frame, "Optimization:", ['min', 'max'], 'min', row_index
        )
        row_index += 1

        # --- Run Button ---
        run_button = ttk.Button(
            main_frame, text="Run Genetic Algorithm", command=self.run_ga
        )
        run_button.grid(
            row=row_index, column=0, columnspan=2, sticky="ew", pady=20
        )
        row_index += 1

        # --- Status Label ---
        self.status_label = ttk.Label(main_frame, text="Ready.")
        self.status_label.grid(
            row=row_index, column=0, columnspan=2, sticky="w", pady=5
        )

        # Configure column weights so entry boxes expand
        main_frame.columnconfigure(1, weight=1)

    def _create_entry(self, parent, text, default_value, row):
        """Helper function to create a Label and an Entry widget."""
        ttk.Label(parent, text=text).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        entry = ttk.Entry(parent)
        entry.insert(0, str(default_value))
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        return entry

    def _create_combo(self, parent, text, values, default_value, row):
        """Helper function to create a Label and a Combobox widget."""
        ttk.Label(parent, text=text).grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        combo = ttk.Combobox(parent, values=values, state="readonly")
        combo.set(default_value)
        combo.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        return combo

    def run_ga(self):
        """Gathers data from the GUI, builds config, and runs the GA."""
        try:
            # --- 1. Gather all values from GUI ---
            
            # Get benchmark function class
            func_name = self.widgets['benchmark'].get()
            benchmark_func_class = self.benchmark_functions[func_name]
            
            # Get main run parameter
            epochs = int(self.widgets['epochs'].get())
            
            # Get config parameters
            pop_size = int(self.widgets['population_size'].get())
            n_vars = int(self.widgets['n_variables'].get())
            precision = int(self.widgets['precision'].get())
            p_mut = float(self.widgets['p_mutation'].get())
            p_inv = float(self.widgets['p_inversion'].get())
            elite_p = float(self.widgets['elite_p'].get())
            
            # Build the bounds list dynamically
            min_b = float(self.widgets['bound_min'].get())
            max_b = float(self.widgets['bound_max'].get())
            bounds = [(min_b, max_b)] * n_vars # e.g., [(-3, 4), (-3, 4)]
            
            crossover = self.widgets['crossover_method'].get()
            mutation = self.widgets['mutation_method'].get()
            optimization = self.widgets['optimization'].get()

            # --- 2. Build the config dictionary ---
            config = {
                'population_size': pop_size,
                'n_variables': n_vars,
                'bounds': bounds,
                'precision': precision,
                'p_mutation': p_mut,
                'p_inversion': p_inv,
                'elite_p': elite_p,
                'crossover_method': crossover,
                'mutation_method': mutation,
                'optimization': optimization
            }

            # --- 3. Run the Genetic Algorithm ---
            self.status_label.config(
                text=f"Running GA with {func_name} for {epochs} epochs...\n\n\n"
            )
            self.update_idletasks() # Force GUI to update

            print("="*30)
            print(f"Starting GA Run: {func_name}")
            print(f"Config: {config}")
            print(f"Epochs: {epochs}")
            print("="*30)

            # Instantiate the GA
            # We instantiate the benchmark function: bf.McCormick()
            ga = GeneticAlgorithm(config, benchmark_func_class())

            # Run the GA
            winner = ga.run(epochs=epochs)
            
            print("--- GA Run Finished ---")
            
            self.status_label.config(
                #text="Run finished! Check console for results."
                text=f"Run finished!\nBest solution: {winner.decode()}\nFitness: {winner.fitness:.2f}"
            )

        except ValueError as e:
            # Handle errors like typing 'abc' into an 'int' field
            messagebox.showerror("Invalid Input", f"Error: {e}\nPlease check all input fields.")
            self.status_label.config(text="Error: Invalid input.")
        except Exception as e:
            # Handle other errors (e.g., from your GA code)
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            self.status_label.config(text=f"Error: {e}")

if __name__ == "__main__":
    app = GeneticAlgorithmGUI()
    app.mainloop()