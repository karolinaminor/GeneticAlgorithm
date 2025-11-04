import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import benchmark_functions as bf

from app_controller import AppController
import plotter 

from genetic_algorithm import GeneticAlgorithm

class GeneticAlgorithmGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genetic Algorithm Runner")
        self.geometry("450x750")

        self.last_run_history = None 
        self.widgets = {}

        self.benchmark_functions = {"McCormick": bf.McCormick}
        
        self.controller = AppController(self, self.benchmark_functions)

        self._create_widgets()

    def _create_widgets(self):
        """All widget creation logic is here."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        row_index = 0

        param_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        param_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew")
        param_row = 0
        
        self.widgets['benchmark'] = self._create_combo(param_frame, "Benchmark Function:", list(self.benchmark_functions.keys()), "McCormick", param_row); param_row += 1
        self.widgets['epochs'] = self._create_entry(param_frame, "Epochs:", 125, param_row); param_row += 1
        self.widgets['population_size'] = self._create_entry(param_frame, "Population Size:", 10, param_row); param_row += 1
        self.widgets['n_variables'] = self._create_entry(param_frame, "Number of Variables:", 2, param_row); param_row += 1
        self.widgets['bound_min'] = self._create_entry(param_frame, "Min Bound (for all):", -3, param_row); param_row += 1
        self.widgets['bound_max'] = self._create_entry(param_frame, "Max Bound (for all):", 4, param_row); param_row += 1
        self.widgets['precision'] = self._create_entry(param_frame, "Precision:", 3, param_row); param_row += 1
        self.widgets['p_mutation'] = self._create_entry(param_frame, "P(mutation):", 0.09, param_row); param_row += 1
        self.widgets['p_inversion'] = self._create_entry(param_frame, "P(inversion):", 0.09, param_row); param_row += 1
        self.widgets['elite_p'] = self._create_entry(param_frame, "Elite Percentage:", 0.15, param_row); param_row += 1
        self.widgets['crossover_method'] = self._create_combo(param_frame, "Crossover Method:", ['one_point', 'two_point', 'uniform'], 'two_point', param_row); param_row += 1
        self.widgets['mutation_method'] = self._create_combo(param_frame, "Mutation Method:", ['one_point', 'multiple_point'], 'one_point', param_row); param_row += 1
        self.widgets['optimization'] = self._create_combo(param_frame, "Optimization:", ['min', 'max'], 'min', param_row); param_row += 1
        self.widgets['db_file'] = self._create_entry(param_frame, "Database File:", "ga_results.db", param_row); param_row += 1
        
        param_frame.columnconfigure(1, weight=1)
        row_index += 1

        run_frame = ttk.Frame(main_frame, padding="5 0")
        run_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew")
        self.run_button = ttk.Button(run_frame, text="Run Genetic Algorithm", command=self.run_ga_clicked)
        self.run_button.pack(fill=tk.X, expand=True)
        row_index += 1
        
        plot_frame = ttk.LabelFrame(main_frame, text="Results and Plots", padding="10")
        plot_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady="10 0")
        self.plot_fitness_button = ttk.Button(plot_frame, text="Plot: Best Fitness Value", command=self.plot_best_fitness, state=tk.DISABLED)
        self.plot_fitness_button.pack(fill=tk.X, expand=True, pady=2)
        self.plot_stats_button = ttk.Button(plot_frame, text="Plot: Average Value and Std. Dev.", command=self.plot_avg_std_dev, state=tk.DISABLED)
        self.plot_stats_button.pack(fill=tk.X, expand=True, pady=2)
        row_index += 1

        self.status_label = ttk.Label(main_frame, text="Ready.", relief=tk.SUNKEN, anchor="nw", wraplength=430)
        self.status_label.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady=5)
        main_frame.columnconfigure(1, weight=1)
        
    def _create_entry(self, parent, text, default_value, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        entry = ttk.Entry(parent)
        entry.insert(0, str(default_value))
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return entry

    def _create_combo(self, parent, text, values, default_value, row):
        ttk.Label(parent, text=text).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        combo = ttk.Combobox(parent, values=values, state="readonly")
        combo.set(default_value)
        combo.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return combo

    
    def run_ga_clicked(self):
        """Called when the 'Run' button is clicked."""
        self.run_button.config(state=tk.DISABLED)
        self.plot_fitness_button.config(state=tk.DISABLED)
        self.plot_stats_button.config(state=tk.DISABLED)
        self.last_run_history = None

        try:
            gui_data = {
                'benchmark': self.widgets['benchmark'].get(),
                'epochs': int(self.widgets['epochs'].get()),
                'pop_size': int(self.widgets['population_size'].get()),
                'n_vars': int(self.widgets['n_variables'].get()),
                'precision': int(self.widgets['precision'].get()),
                'p_mut': float(self.widgets['p_mutation'].get()),
                'p_inv': float(self.widgets['p_inversion'].get()),
                'elite_p': float(self.widgets['elite_p'].get()),
                'min_b': float(self.widgets['bound_min'].get()),
                'max_b': float(self.widgets['bound_max'].get()),
                'crossover': self.widgets['crossover_method'].get(),
                'mutation': self.widgets['mutation_method'].get(),
                'optimization': self.widgets['optimization'].get(),
                'db_file': self.widgets['db_file'].get() or "ga_results.db"
            }
            
            self.controller.run_ga_task(gui_data)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}\nPlease check all input fields.")
            self.on_run_error("Error: Invalid input.")

    def plot_best_fitness(self):
        """Delegates plotting to the plotter module."""
        plotter.plot_best_fitness(self.last_run_history)

    def plot_avg_std_dev(self):
        """Delegates plotting to the plotter module."""
        plotter.plot_avg_std_dev(self.last_run_history)

    def update_status(self, text):
        """Allows the controller to update the status label."""
        self.status_label.config(text=text)
        self.update_idletasks()

    def on_run_complete(self, status_text, history):
        """Called by the controller when the GA run is finished."""
        self.status_label.config(text=status_text)
        self.last_run_history = history
        self.plot_fitness_button.config(state=tk.NORMAL)
        self.plot_stats_button.config(state=tk.NORMAL)
        self.run_button.config(state=tk.NORMAL)
    
    def on_run_error(self, error_text):
        """Called by the controller if an error occurs."""
        self.status_label.config(text=error_text)
        self.run_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    app = GeneticAlgorithmGUI()
    app.mainloop()
    