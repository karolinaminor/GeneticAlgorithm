import matplotlib.pyplot as plt
from tkinter import messagebox

def plot_best_fitness(history):
    """Generates a plot of the best fitness value over epochs."""
    if not history:
        messagebox.showinfo("No Data", "No history data to plot.")
        return
    try:
        epochs = [h['epoch'] for h in history]
        best_fitness = [h['best_fitness'] for h in history]
        
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

def plot_avg_std_dev(history):
    """Generates a plot of the average value and standard deviation."""
    if not history:
        messagebox.showinfo("No Data", "No history data to plot.")
        return
    try:
        epochs = [h['epoch'] for h in history]
        avg_fitness = [h['average_fitness'] for h in history]
        std_dev = [h['std_fitness'] for h in history]
        
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
        