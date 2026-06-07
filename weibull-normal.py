import openpyxl
import numpy as np
from scipy.stats import gamma, weibull_min, norm
import pandas as pd

def simulate_vci_phases(workbook_path, vci_sheet_name="VCI", num_simulations=10000):
    df = pd.read_excel(workbook_path, sheet_name=vci_sheet_name)
    vci_cols = ["LR_P1_VCI", "LR_P2_VCI", "SR_P1_VCI", "SR_P2_VCI"]

    
    best_distributions = {
        "LR_P1_VCI": "Weibull",
        "LR_P2_VCI": "Weibull",
        "SR_P1_VCI": "Normal",
        "SR_P2_VCI": "Normal",
    }

    results = {}
    simulation_data = {}
    epsilon = 1e-9

    np.random.seed(123)

    print(f"{'Phase':<12} | {'Distribution':<12} | {'Param 1':<10} | {'Param 2':<10} | {'Loc':<10} | {'Mean':<10} | {'Variance':<10}")
    print("-" * 100)

    for col in vci_cols:
        if col not in df.columns:
            print(f"Skipping {col}: Column not found in Excel.")
            continue

        data = df[col].dropna().values
        data = np.where(data <= 0, epsilon, data)
         

        if len(data) < 2:
            print(f"Skipping {col}: Not enough data points.")
            continue

        dist_name = best_distributions[col]

        #  Weibull (LR columns)
        if dist_name == "Weibull":
            fitted = weibull_min.fit(data)
            shape, loc, scale = fitted
            mean = weibull_min.mean(*fitted)
            variance = weibull_min.var(*fitted)

            results[col] = {
                "distribution": dist_name,
                "shape (c)": shape,
                "loc": loc,
                "scale": scale,
                "mean": mean,
                "variance": variance,
            }

            print(f"{col:<12} | {dist_name:<12} | {shape:10.4f} | {scale:10.4f} | {loc:10.4f} | {mean:10.4f} | {variance:10.4f}")

            simulated_data = weibull_min.rvs(*fitted, size=num_simulations)

        #  Normal (SR columns)
        elif dist_name == "Normal":
            fitted = norm.fit(data)
            mu, sigma = fitted
            mean = mu
            variance = sigma ** 2

            results[col] = {
                "distribution": dist_name,
                "mean (mu)": mu,
                "std (sigma)": sigma,
                "loc": mu,        # for consistency in the table
                "scale": sigma,
                "mean": mean,
                "variance": variance,
            }

            print(f"{col:<12} | {dist_name:<12} | {mu:10.4f} | {sigma:10.4f} | {'N/A':>10} | {mean:10.4f} | {variance:10.4f}")

            simulated_data = norm.rvs(loc=mu, scale=sigma, size=num_simulations)

        
        simulated_data = np.clip(simulated_data, 0, 1)
        simulation_data[col] = simulated_data

    # Save to Excel 
    with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        param_df = pd.DataFrame(results).T
        param_df.to_excel(writer, sheet_name="VCI_Parameters")

        sim_df = pd.DataFrame(simulation_data)
        sim_df.to_excel(writer, sheet_name="VCI_Simulations(web,norm)", index=False)

    print(f"\nSuccess — Parameters and {num_simulations} simulations saved to {workbook_path}")


if __name__ == "__main__":
    path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_NDVI_final.xlsx"
    simulate_vci_phases(path)