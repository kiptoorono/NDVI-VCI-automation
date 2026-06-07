import openpyxl
import numpy as np
import pandas as pd
from scipy.stats import gamma

def simulate_spi_directly(workbook_path, spi_sheet_name="SPI", num_simulations=10000):
    df = pd.read_excel(workbook_path, sheet_name=spi_sheet_name)
    spi_cols = ["LR_P1_Z", "LR_P2_Z", "SR_P1_Z", "SR_P2_Z"]
    
    results = {}
    simulation_data = {}
    epsilon = 1e-9 

    print(f"{'Phase':<12} | {'Shape (α)':<10} | {'Scale (θ)':<10}")
    print("-" * 40)

    for col in spi_cols:
        if col not in df.columns:
            continue
        raw_data = df[col].dropna().values
        

        positive_data = np.where(raw_data <= 0, epsilon, raw_data)
        positive_data = np.clip(positive_data, epsilon, 1.0)
        
        # Shape/Scale using Population Variance
        mu = np.mean(positive_data)
        var = np.var(positive_data, ddof=0)
        
        # Method of Moments
        shape = (mu ** 2) / var if var > 0 else 1.0
        scale = var / mu if mu > 0 else epsilon
        
        print(f"{col:<12} | {shape:10.4f} | {scale:10.4f}")

        # Simulate 
        sim_results = gamma.rvs(shape, loc=0, scale=scale, size=num_simulations)
        
        #  Apply capping: 
        simulation_data[col] = np.clip(sim_results, epsilon, 1.0)
        
        results[col] = {"shape": shape, "scale": scale, "mean": mu, "variance": var}

    # Save to Excel
    with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        pd.DataFrame(results).T.to_excel(writer, sheet_name="SPI_Gamma_Params")
        pd.DataFrame(simulation_data).to_excel(writer, sheet_name="SPI_Sim_Results", index=False)

    print(f"\nSuccess! Capped SPI Simulations (0-1) saved to {workbook_path}")

if __name__ == "__main__":
    path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_CHIRP_MeanDailyRainfall_final.csv.xlsx"
    simulate_spi_directly(path)