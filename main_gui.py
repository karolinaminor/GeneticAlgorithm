import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import json
import datetime

import matplotlib.pyplot as plt

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
        self.geometry("450x750")

        # Stores the history from the last run
        self.last_run_history = None 

        self.benchmark_functions = {
            "McCormick": bf.McCormick,
        }
        
        self.widgets = {}

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        row_index = 0

        # parameters
        param_frame = ttk.LabelFrame(main_frame, text="Parameters", padding="10")
        param_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew")
        
        param_row = 0

        self.widgets['benchmark'] = self._create_combo(
            param_frame, "Benchmark Function:",
            list(self.benchmark_functions.keys()), "McCormick", param_row
        )
        param_row += 1

        self.widgets['epochs'] = self._create_entry(
            param_frame, "Epochs:", 125, param_row
        )
        param_row += 1
        
        self.widgets['population_size'] = self._create_entry(
            param_frame, "Population Size:", 10, param_row
        )
        param_row += 1
        
        self.widgets['n_variables'] = self._create_entry(
            param_frame, "Number of Variables:", 2, param_row
        )
        param_row += 1

        self.widgets['bound_min'] = self._create_entry(
            param_frame, "Min Bound (for all):", -3, param_row
        )
        param_row += 1
        self.widgets['bound_max'] = self._create_entry(
            param_frame, "Max Bound (for all):", 4, param_row
        )
        param_row += 1
        
        self.widgets['precision'] = self._create_entry(
            param_frame, "Precision:", 3, param_row
        )
        param_row += 1
        
        self.widgets['p_mutation'] = self._create_entry(
            param_frame, "P(mutation):", 0.09, param_row
        )
        param_row += 1

        self.widgets['p_inversion'] = self._create_entry(
            param_frame, "P(inversion):", 0.09, param_row
        )
        param_row += 1
        
        self.widgets['elite_p'] = self._create_entry(
            param_frame, "Elite Percentage:", 0.15, param_row
        )
        param_row += 1

        crossover_options = ['one_point', 'two_point', 'uniform']
        self.widgets['crossover_method'] = self._create_combo(
            param_frame, "Crossover Method:", crossover_options, 'two_point', param_row
        )
        param_row += 1

        mutation_options = ['one_point', 'multiple_point']
        self.widgets['mutation_method'] = self._create_combo(
            param_frame, "Mutation Method:", mutation_options, 'one_point', param_row
        )
        param_row += 1

        self.widgets['optimization'] = self._create_combo(
            param_frame, "Optimization:", ['min', 'max'], 'min', param_row
        )
        param_row += 1
        
        self.widgets['db_file'] = self._create_entry(
            param_frame, "Database File:", "ga_results.db", param_row
        )
        param_row += 1
        
        param_frame.columnconfigure(1, weight=1)
        row_index += 1

        # run
        run_frame = ttk.Frame(main_frame, padding="5 0")
        run_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew")

        self.run_button = ttk.Button(
            run_frame, text="Run Genetic Algorithm", command=self.run_ga
        )
        self.run_button.pack(fill=tk.X, expand=True)
        row_index += 1
        
        # plots
        plot_frame = ttk.LabelFrame(main_frame, text="Results and Plots", padding="10")
        plot_frame.grid(row=row_index, column=0, columnspan=2, sticky="ew", pady="10 0")

        self.plot_fitness_button = ttk.Button(
            plot_frame, text="Plot: Best Fitness Value",
            command=self.plot_best_fitness, state=tk.DISABLED
        )
        self.plot_fitness_button.pack(fill=tk.X, expand=True, pady=2)

        self.plot_stats_button = ttk.Button(
            plot_frame, text="Plot: Average Value and Std. Dev.",
            command=self.plot_avg_std_dev, state=tk.DISABLED
        )
        self.plot_stats_button.pack(fill=tk.X, expand=True, pady=2)
        row_index += 1

        # status
        self.status_label = ttk.Label(main_frame, text="Ready.", relief=tk.SUNKEN, anchor="nw", wraplength=430)#, height=4)
        self.status_label.grid(
            row=row_index, column=0, columnspan=2, sticky="ew", pady=5
        )

        main_frame.columnconfigure(1, weight=1)

    def _create_entry(self, parent, text, default_value, row):
        ttk.Label(parent, text=text).grid(
            row=row, column=0, sticky="w", padx=5, pady=3
        )
        entry = ttk.Entry(parent)
        entry.insert(0, str(default_value))
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return entry

    def _create_combo(self, parent, text, values, default_value, row):
        ttk.Label(parent, text=text).grid(
            row=row, column=0, sticky="w", padx=5, pady=3
        )
        combo = ttk.Combobox(parent, values=values, state="readonly")
        combo.set(default_value)
        combo.grid(row=row, column=1, sticky="ew", padx=5, pady=3)
        return combo

    def _init_db(self):
        """Create database file and table if not exists."""
        conn = sqlite3.connect("results.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ga_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                function_name TEXT,
                epoch INTEGER,
                best_fitness REAL,
                best_solution TEXT
            )
        """)
        conn.commit()
        conn.close()

    def _save_result(self, function_name, epoch, best_fitness, best_solution):
        """Save one iteration's result to the database."""
        conn = sqlite3.connect("results.db")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ga_results (function_name, epoch, best_fitness, best_solution) VALUES (?, ?, ?, ?)",
            (function_name, epoch, best_fitness, str(best_solution))
        )
        conn.commit()
        conn.close()

    def run_ga(self):
        try:
            self.run_button.config(state=tk.DISABLED)
            self.plot_fitness_button.config(state=tk.DISABLED)
            self.plot_stats_button.config(state=tk.DISABLED)
            self.last_run_history = None
            
            func_name = self.widgets['benchmark'].get()
            benchmark_func_class = self.benchmark_functions[func_name]
            epochs = int(self.widgets['epochs'].get())
            pop_size = int(self.widgets['population_size'].get())
            n_vars = int(self.widgets['n_variables'].get())
            precision = int(self.widgets['precision'].get())
            p_mut = float(self.widgets['p_mutation'].get())
            p_inv = float(self.widgets['p_inversion'].get())
            elite_p = float(self.widgets['elite_p'].get())
            min_b = float(self.widgets['bound_min'].get())
            max_b = float(self.widgets['bound_max'].get())
            bounds = [(min_b, max_b)] * n_vars
            crossover = self.widgets['crossover_method'].get()
            mutation = self.widgets['mutation_method'].get()
            optimization = self.widgets['optimization'].get()

            config = {
                'population_size': pop_size, 'n_variables': n_vars,
                'bounds': bounds, 'precision': precision, 'p_mutation': p_mut,
                'p_inversion': p_inv, 'elite_p': elite_p,
                'crossover_method': crossover, 'mutation_method': mutation,
                'optimization': optimization
            }

            self.status_label.config(
                text=f"Running GA with {func_name} for {epochs} epochs..."
            )
            self.update_idletasks()

            print("=" * 30)
            print(f"Starting GA Run: {func_name}")
            print(f"Config: {config}")
            print(f"Epochs: {epochs}")
            print("=" * 30)

            ga = GeneticAlgorithm(config, benchmark_func_class())

            winner, history = ga.run(epochs=epochs)
            
            self.last_run_history = history
            
            print("--- GA Run Finished ---")
            
            db_file = self.save_results_to_db(config, epochs, func_name, history)

            self.status_label.config(
                text=f"Run finished!\nBest solution: {winner.decode()}\n"
                     f"Fitness: {winner.fitness:.4f}\nResults saved to {db_file}"
            )
            
            self.plot_fitness_button.config(state=tk.NORMAL)
            self.plot_stats_button.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}\nPlease check all input fields.")
            self.status_label.config(text="Error: Invalid input.")
        except TypeError as e:
             if "'NoneType' is not iterable" in str(e):
                messagebox.showerror(
                    "GA Implementation Error", 
                    "The `ga.run()` method probably did not return a history.\n\n"
                    "Expected: `winner, history = ga.run(...)`\n"
                    f"Received error: {e}\n\n"
                    "Please update `genetic_algorithm.py`."
                )
                self.status_label.config(text="Error: `ga.run()` did not return history.")
             else:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
                self.status_label.config(text=f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            self.status_label.config(text=f"Error: {e}")
        
        finally:
            self.run_button.config(state=tk.NORMAL)

    def save_results_to_db(self, config, epochs, func_name, history):
        """Saves the run results to an SQLite database."""
        db_file = self.widgets['db_file'].get()
        if not db_file:
            db_file = "ga_results.db"
            
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            benchmark_function TEXT NOT NULL,
            epochs INTEGER NOT NULL,
            config_json TEXT NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            epoch INTEGER NOT NULL,
            best_fitness REAL NOT NULL,
            avg_fitness REAL NOT NULL,
            std_dev REAL NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
        """)

        run_time = datetime.datetime.now().isoformat()
        config_to_save = config.copy()
        config_to_save['bounds'] = list(config_to_save['bounds'])
        config_str = json.dumps(config_to_save, indent=2)
        
        cursor.execute(
            "INSERT INTO runs (timestamp, benchmark_function, epochs, config_json) VALUES (?, ?, ?, ?)",
            (run_time, func_name, epochs, config_str)
        )
        run_id = cursor.lastrowid

        if not history or not isinstance(history, list) or not isinstance(history[0], dict):
             raise TypeError("History format is incorrect. Expected a list of dictionaries.")

        results_data = [
            (run_id, h['epoch'], h['best_fitness'], h['average_fitness'], h['std_fitness'])
            for h in history
        ]
        
        cursor.executemany(
            "INSERT INTO results (run_id, epoch, best_fitness, avg_fitness, std_dev) VALUES (?, ?, ?, ?, ?)",
            results_data
        )

        conn.commit()
        conn.close()
        
        print(f"Results successfully saved to {db_file} (Run ID: {run_id})")
        return db_file

    def plot_best_fitness(self):
        """Generates a plot of the best fitness value over epochs."""
        if not self.last_run_history:
            messagebox.showinfo("No Data", "Run the algorithm first.")
            return

        try:
            epochs = [h['epoch'] for h in self.last_run_history]
            best_fitness = [h['best_fitness'] for h in self.last_run_history]
            
            plt.figure(figsize=(10, 6))
            plt.plot(epochs, best_fitness, marker='.', linestyle='-')
            plt.title("Best Fitness Value vs. Epoch")
            plt.xlabel("Epoch")
            plt.ylabel("Fitness Value")
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            messagebox.showerror("Plot Error", f"Could not generate plot: {e}")

    def plot_avg_std_dev(self):
        """Generates a plot of the average value and standard deviation."""
        if not self.last_run_history:
            messagebox.showinfo("No Data", "Run the algorithm first.")
            return
            
        try:
            epochs = [h['epoch'] for h in self.last_run_history]
            avg_fitness = [h['average_fitness'] for h in self.last_run_history]
            std_dev = [h['std_fitness'] for h in self.last_run_history]
            
            avg_plus_std = [a + s for a, s in zip(avg_fitness, std_dev)]
            avg_minus_std = [a - s for a, s in zip(avg_fitness, std_dev)]
            
            plt.figure(figsize=(10, 6))
            
            plt.plot(epochs, avg_fitness, marker='.', linestyle='-', label='Average Fitness Value')
            
            plt.fill_between(
                epochs, avg_minus_std, avg_plus_std, 
                color='blue', alpha=0.2, label='Standard Deviation (±1 std)'
            )
            
            plt.title("Average Fitness and Standard Deviation vs. Epoch")
            plt.xlabel("Epoch")
            plt.ylabel("Fitness Value")
            plt.legend()
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Plot Error", f"Could not generate plot: {e}")


if __name__ == "__main__":
    app = GeneticAlgorithmGUI()
    app.mainloop()
    