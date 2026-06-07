import pandas as pd
import numpy as np
from scipy.stats import gamma
import tkinter as tk
from tkinter import filedialog, messagebox

def run_simulation(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name="SPI")
        spi_cols = ["LR_P1_Z", "LR_P2_Z", "SR_P1_Z", "SR_P2_Z"]
        
        results, simulation_data = {}, {}
        epsilon = 1e-9 
        num_simulations = 10000

        for col in spi_cols:
            if col not in df.columns: continue
            
            raw_data = df[col].dropna().values
            # Apply your requested capping (0-1) and epsilon
            positive_data = np.clip(np.where(raw_data <= 0, epsilon, raw_data), epsilon, 1.0)
            
            mu, var = np.mean(positive_data), np.var(positive_data, ddof=0)
            shape = (mu ** 2) / var if var > 0 else 1.0
            scale = var / mu if mu > 0 else epsilon
            
            sim_results = gamma.rvs(shape, loc=0, scale=scale, size=num_simulations)
            simulation_data[col] = np.clip(sim_results, epsilon, 1.0)
            results[col] = {"shape": shape, "scale": scale, "mean": mu}

        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            pd.DataFrame(results).T.to_excel(writer, sheet_name="SPI_Gamma_Params")
            pd.DataFrame(simulation_data).to_excel(writer, sheet_name="SPI_Sim_Results", index=False)
        
        return True
    except Exception as e:
        return str(e)

def select_file():
    path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if path:
        status_label.config(text="Processing... please wait.", fg="blue")
        root.update()
        success = run_simulation(path)
        if success is True:
            messagebox.showinfo("Success", f"Simulations saved to:\n{path}")
        else:
            messagebox.showerror("Error", f"Failed: {success}")
        status_label.config(text="Waiting for file...", fg="black")

# Simple UI Window
root = tk.Tk()
root.title("SPI Gamma Simulator v1.0")
root.geometry("400x200")

tk.Label(root, text="Gamma Simulation Tool", font=("Arial", 14, "bold")).pack(pady=10)
tk.Button(root, text="Select Excel File & Run", command=select_file, height=2, width=25, bg="green", fg="white").pack(pady=20)
status_label = tk.Label(root, text="Waiting for file...")
status_label.pack()

root.mainloop()