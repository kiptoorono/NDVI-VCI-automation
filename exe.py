import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import pandas as pd

# 
script_dir = os.path.dirname(os.path.abspath(__file__))
new_folder_path = os.path.abspath(os.path.join(script_dir, '..', 'New'))
sys.path.append(new_folder_path)

# Import individual modules
try:
    import summation
    import standardise_SPI
    import VCI
    import VCI_simulation
except ImportError as e:
    print(f"Import Error: {e}. Ensure filenames in 'New' folder have no spaces.")

class SimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Automation Tool")
        self.root.geometry("450x600")
        self.selected_path = None  # Persistent file path

        # --- SECTION 1: FILE SELECTION ---
        tk.Label(root, text="Step 1: Select Workbook", font=("Arial", 11, "bold")).pack(pady=10)
        
        self.btn_browse = tk.Button(root, text="Browse Excel File", command=self.browse_file, 
                                    bg="#3498db", fg="white", width=20)
        self.btn_browse.pack(pady=5)
        
        self.path_label = tk.Label(root, text="No file selected", fg="red", wraplength=400)
        self.path_label.pack(pady=5)

        tk.Canvas(root, height=2, bg="lightgrey", highlightthickness=0).pack(fill="x", padx=20, pady=10)

        # ---  ---
        tk.Label(root, text="Step 2: Run Specific Tasks", font=("Arial", 11, "bold")).pack(pady=5)
        
        self.btn_sum = tk.Button(root, text="1. Run Summation", command=lambda: self.execute(summation.run_payout_gamma_simulation), width=35)
        self.btn_sum.pack(pady=5)
        
        self.btn_std = tk.Button(root, text="2. Standardize SPI", command=lambda: self.execute(standardise_SPI.simulate_spi_directly), width=35)
        self.btn_std.pack(pady=5)
        
        self.btn_vci = tk.Button(root, text="3. Calculate VCI", command=lambda: self.execute(VCI.simulate_vci_phases), width=35)
        self.btn_vci.pack(pady=5)
        
        self.btn_sim = tk.Button(root, text="4. VCI Simulation", command=lambda: self.execute(VCI_simulation.simulate_vci_phases), width=35)
        self.btn_sim.pack(pady=5)

        # --- SEMASTER ACTION ---
        tk.Label(root, text="--- OR ---").pack(pady=10)

        self.btn_all = tk.Button(root, text="RUN FULL PIPELINE (1-4)", command=self.run_all, 
                                 bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2, width=35)
        self.btn_all.pack(pady=10)

        self.status = tk.Label(root, text="Ready", fg="grey")
        self.status.pack(side="bottom", pady=20)

    def browse_file(self):
        """Selects the file and updates the UI label."""
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.selected_path = path
            self.path_label.config(text=f"Selected: {os.path.basename(path)}", fg="green")
            self.status.config(text="File Loaded. Ready to run.", fg="black")

    def execute(self, func):
        """Runs a single function using the pre-selected path."""
        if not self.selected_path:
            messagebox.showwarning("No File", "Please select an Excel file first!")
            return

        try:
            self.status.config(text="Processing Task...", fg="blue")
            self.root.update()
            func(self.selected_path) 
            messagebox.showinfo("Success", "Task completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.status.config(text="Ready", fg="grey")

    def run_all(self):
        """Runs all scripts in sequence using the pre-selected path."""
        if not self.selected_path:
            messagebox.showwarning("No File", "Please select an Excel file first!")
            return

        try:
            tasks = [
                ("Summation", summation.run_payout_gamma_simulation),
                ("Standardizing", standardise_SPI.simulate_spi_directly),
                ("VCI Calculation", VCI.simulate_vci_phases),
                ("Final Simulation", VCI_simulation.simulate_vci_phases)
            ]
            
            for name, func in tasks:
                self.status.config(text=f"Running {name}...", fg="blue")
                self.root.update()
                func(self.selected_path)
            
            messagebox.showinfo("Success", "Full pipeline executed successfully!")
        except Exception as e:
            messagebox.showerror("Pipeline Error", str(e))
        finally:
            self.status.config(text="Ready", fg="grey")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulationApp(root)
    root.mainloop()