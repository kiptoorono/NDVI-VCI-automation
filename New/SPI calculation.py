import openpyxl
import statistics
from pathlib import Path

def analyze_rainfall_with_dual_sheets(
    workbook_path: str,
    source_sheet: str = "Dekadal_Data",
    sums_sheet_name: str = "dekad_sums",
    transposed_sheet_name: str = "SPI",
    header: bool = True,
    index_col: bool = True):
    # Load Workbook
    try:
        wb = openpyxl.load_workbook(workbook_path, data_only=True)
    except Exception as e:
        raise PermissionError(f"Error loading workbook: {e}")

    src = wb[source_sheet] if source_sheet in wb.sheetnames else wb[wb.sheetnames[0]]

    start_col = 2 if index_col else 1
    max_col = src.max_column
    base_row = 1 if header else 0

    # Extract and Filter Year Labels (Up to 2025)
    cols = list(range(start_col, max_col + 1))
    valid_cols, valid_labels = [], []
    for c in cols:
        lbl = src.cell(row=1, column=c).value
        try:
            if int(str(lbl)) <= 2025:
                valid_cols.append(c)
                valid_labels.append(lbl)
        except:
            valid_cols.append(c)
            valid_labels.append(lbl)

    # Phases (LR: 9-17, SR: 18-36)
    seasons = {
        "LR_P1": (9, 13),
        "LR_P2": (14, 17),
        "SR_P1": (18, 27),
        "SR_P2": (28, 36)
    }

    # Helper to sum values vertically
    def get_sums(start_d, end_d):
        res = []
        for c in valid_cols:
            vals = []
            for r in range(base_row + start_d, base_row + end_d + 1):
                cell_val = src.cell(row=r, column=c).value
                try:
                    vals.append(float(cell_val))
                except (TypeError, ValueError):
                    continue
            res.append(sum(vals) if vals else 0.0)
        return res

    #Calculate All Statistics
    results = {}
    for name, d_range in seasons.items():
        sums = get_sums(*d_range)
        mu = statistics.mean(sums)
        sigma = statistics.pstdev(sums)
        z_scores = [(x - mu) / sigma if sigma > 0 else 0.0 for x in sums]
        
        results[name] = {
            "sums": sums,
            "mu": mu,
            "sigma": sigma,
            "z": z_scores
        }

    # --- VERIFICATION PRINT ---
    print("\n" + "="*65)
    print(f"{'Phase':<10} | {'Historical Mean':<18} | {'Pop Std Dev':<15}")
    print("-" * 65)
    for name, data in results.items():
        print(f"{name:<10} | {data['mu']:<18.4f} | {data['sigma']:<15.4f}")
    print("="*65 + "\n")

    # DEKAD SUMS (Horizontal style)
    if sums_sheet_name in wb.sheetnames:
        del wb[sums_sheet_name]
    ws_sums = wb.create_sheet(sums_sheet_name)
    ws_sums.append(["Phase Range"] + valid_labels)
    for name, d_range in seasons.items():
        ws_sums.append([f"{name}({d_range[0]}-{d_range[1]})"] + results[name]["sums"])

    # SPI ANALYSIS (Transposed with summary stats)
    if transposed_sheet_name in wb.sheetnames:
        del wb[transposed_sheet_name]
    ws_trans = wb.create_sheet(transposed_sheet_name)
    
    # Header: Year, then all 4 Sums, 2 blanks, then all 4 Z-scores
    ws_trans.append([
        "Year",
        "LR_P1_Sum", "LR_P2_Sum", "SR_P1_Sum", "SR_P2_Sum",
        "", "", 
        "LR_P1_Z", "LR_P2_Z", "SR_P1_Z", "SR_P2_Z"
    ])

    # Append year-by-year data
    for i in range(len(valid_labels)):
        row = [valid_labels[i]]
        row += [results[p]["sums"][i] for p in seasons.keys()]
        row += ["", ""]
        row += [results[p]["z"][i] for p in seasons.keys()]
        ws_trans.append(row)

    # Append Summary Statistics at the bottom
    ws_trans.append([]) 
    
    mean_row = ["Mean"] + [results[p]["mu"] for p in seasons.keys()] + ["", ""] + ["", "", "", ""]
    ws_trans.append(mean_row)

    std_row = ["Std Dev (Pop)"] + [results[p]["sigma"] for p in seasons.keys()] + ["", ""] + ["", "", "", ""]
    ws_trans.append(std_row)

    # Save
    wb.save(workbook_path)
    return workbook_path

if __name__ == "__main__":
    path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_CHIRP_MeanDailyRainfall_final.csv.xlsx"
    analyze_rainfall_with_dual_sheets(path)
    print("Process complete. 'dekad_sums' and 'rainfall_SPI_analysis' sheets created.")