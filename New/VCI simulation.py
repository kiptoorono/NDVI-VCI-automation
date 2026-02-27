import openpyxl
import numpy as np
from scipy.stats import gamma
import pandas as pd

def simulate_vci_phases(workbook_path, vci_sheet_name="VCI", num_simulations=10000):
    # 1. Load the VCI data
    # We use pandas for easier statistical fitting, but openpyxl works too
    df = pd.read_excel(workbook_path, sheet_name=vci_sheet_name)
    
    # Identify VCI columns (skipping the NDVIs and spacer columns)
    # Based on your previous code, these are columns: LR_P1_VCI, LR_P2_VCI, SR_P1_VCI, SR_P2_VCI
    vci_cols = ["LR_P1_VCI", "LR_P2_VCI", "SR_P1_VCI", "SR_P2_VCI"]
    
    results = {}
    simulation_data = {}

    print(f"{'Phase':<10} | {'Shape (α)':<10} | {'Scale (θ)':<10}")
    print("-" * 40)

    for col in vci_cols:
        # Clean data: Remove NaNs and ensure values are slightly positive 
        # (Gamma distribution requires values > 0)
        data = df[col].dropna().values
        data = data[data > 0] 
        
        if len(data) < 2:
            print(f"Skipping {col}: Not enough data points.")
            continue

        # 2. Calculate Shape and Scale using Maximum Likelihood Estimation
        # flock=0 fixes the location parameter to 0, which is standard for VCI
        shape, loc, scale = gamma.fit(data, floc=0)
        
        results[col] = {"shape": shape, "scale": scale}
        print(f"{col:<10} | {shape:10.4f} | {scale:10.4f}")

        # 3. Perform 10,000 simulations
        sim_results = gamma.rvs(shape, loc=0, scale=scale, size=num_simulations)
        simulation_data[col] = sim_results

    # 4. Save results to a new sheet
    with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        # Save the parameters
        param_df = pd.DataFrame(results).T
        param_df.to_excel(writer, sheet_name="VCI_Parameters")
        
        # Save a sample of simulations (or all)
        sim_df = pd.DataFrame(simulation_data)
        sim_df.to_excel(writer, sheet_name="VCI_Simulations", index=False)

    print(f"\nSuccess! Parameters and {num_simulations} simulations saved to {workbook_path}")

if __name__ == "__main__":
    path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_NDVI_final.xlsx"
    simulate_vci_phases(path)