# app_controller.py
from tkinter import messagebox
from genetic_algorithm import GeneticAlgorithm
from database_manager import DatabaseManager

class AppController:
    def __init__(self, view, benchmark_functions):
        self.view = view
        self.benchmark_functions = benchmark_functions
        self.db_manager = None

    def run_ga_task(self, gui_data):
        """The main application logic, separate from the GUI."""
        try:
            self.db_manager = DatabaseManager(gui_data['db_file'])

            func_name = gui_data['benchmark']
            benchmark_func_class = self.benchmark_functions[func_name]

            config = {
                'population_size': gui_data['pop_size'],
                'n_variables': gui_data['n_vars'],
                'bounds': [(gui_data['min_b'], gui_data['max_b'])] * gui_data['n_vars'],
                'precision': gui_data['precision'],
                'p_mutation': gui_data['p_mut'],
                'p_inversion': gui_data['p_inv'],
                'elite_p': gui_data['elite_p'],
                'crossover_method': gui_data['crossover'],
                'mutation_method': gui_data['mutation'],
                'optimization': gui_data['optimization']
            }

            self.view.update_status(f"Running GA with {func_name} for {gui_data['epochs']} epochs...")
            
            print("=" * 30)
            print(f"Starting GA Run: {func_name}")
            print(f"Config: {config}")
            print(f"Epochs: {gui_data['epochs']}")
            print("=" * 30)

            ga = GeneticAlgorithm(config, benchmark_func_class())
            winner, history = ga.run(epochs=gui_data['epochs'])
            
            print("--- GA Run Finished ---")
            
            self.db_manager.save_run_results(config, gui_data['epochs'], func_name, history)

            status_text = (
                f"Run finished!\nBest solution: {winner.decode()}\n"
                f"Fitness: {winner.fitness:.4f}\nResults saved to {gui_data['db_file']}"
            )
            self.view.on_run_complete(status_text, history)

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}\nPlease check all input fields.")
            self.view.on_run_error("Error: Invalid input.")
        except TypeError as e:
            if "'NoneType' is not iterable" in str(e):
                messagebox.showerror(
                    "GA Implementation Error", 
                    "The `ga.run()` method probably did not return a history.\n\n"
                    "Expected: `winner, history = ga.run(...)`\n"
                    f"Received error: {e}\n\n"
                    "Please update `genetic_algorithm.py`."
                )
                self.view.on_run_error("Error: `ga.run()` did not return history.")
            else:
                messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
                self.view.on_run_error(f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")
            self.view.on_run_error(f"Error: {e}")
            