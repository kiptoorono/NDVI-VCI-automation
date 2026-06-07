import openpyxl
import numpy as np
from scipy.stats import gamma
import pandas as pd

def stress_sigmoid(x, q_tail, sigma=1.15):
    """
    Compresses tail values upward toward 1 by shrinking the distance to 1.

    sigma  : stress factor — fixed at 1.15
    q_tail : percentile threshold where tail begins (0.90 = top 10% stressed)
    """
    x = x.copy()

    # Identify tail values
    threshold = np.percentile(x, q_tail * 100)
    tail_mask = x >= threshold

    #  Compress tail values toward 1
    tail_vals = x[tail_mask]
    distance_to_1 = 1.0 - tail_vals
    compressed = 1.0 - (distance_to_1 / sigma)

    # Apply and cap at 1
    x[tail_mask] = np.minimum(compressed, 1.0)

    return x


def simulate_vci_phases(workbook_path, vci_sheet_name="VCI", num_simulations=10000):

    sigma  = 1.25   # fixed stress factor: squeezes top tail toward 1.0
    q_tail = 0.90   # top 10% of simulated values

    df = pd.read_excel(workbook_path, sheet_name=vci_sheet_name)
    vci_cols = ["LR_P1_VCI", "LR_P2_VCI", "SR_P1_VCI", "SR_P2_VCI"]

    results = {}
    simulation_data = {}
    epsilon = 1e-9

    np.random.seed(123)

    print(f"{'Phase':<12} | {'Shape (α)':<10} | {'Scale (θ)':<10} | {'Loc':<10} | {'Mean':<10} | {'Variance':<10}")
    print("-" * 80)

    for col in vci_cols:
        if col not in df.columns:
            print(f"Skipping {col}: Column not found in Excel.")
            continue

        data = df[col].dropna().values
        data = np.where(data <= 0, epsilon, data)

        if len(data) < 2:
            print(f"Skipping {col}: Not enough data points.")
            continue

        # --- Fit Gamma ---
        fitted_distribution = gamma.fit(data)
        shape, loc, scale = fitted_distribution

        mean     = shape * scale + loc
        variance = shape * scale ** 2

        results[col] = {
            "shape": shape, "scale": scale, "loc": loc,
            "mean": mean, "variance": variance,
            "sigma": sigma, "q_tail": q_tail
        }

        print(f"{col:<12} | {shape:10.4f} | {scale:10.4f} | {loc:10.4f} | {mean:10.4f} | {variance:10.4f}")

        #  Simulate 
        simulated_data = gamma.rvs(*fitted_distribution, size=num_simulations)
        simulated_data = np.minimum(simulated_data, 1.0)  # initial cap at 1

        #  Apply Tail Compression 
        simulated_data = stress_sigmoid(simulated_data, sigma=sigma, q_tail=q_tail)

        simulation_data[col] = simulated_data

    with pd.ExcelWriter(workbook_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        param_df = pd.DataFrame(results).T
        param_df.to_excel(writer, sheet_name="VCI_Parameters")

        sim_df = pd.DataFrame(simulation_data)
        sim_df.to_excel(writer, sheet_name="VCI_Simulations_blowout_1.25", index=False)

    print(f"\nTail compression applied: sigma={sigma}, q_tail={q_tail}")
    print(f"Success — Parameters and {num_simulations} simulations saved to {workbook_path}")


if __name__ == "__main__":
    path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_NDVI_final.xlsx"
    simulate_vci_phases(path)