import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'Combine_UAI_Final_NDVI_final.xlsx'
xl = pd.ExcelFile(file_path)

# Load the specific sheets
df_zscore = xl.parse('zscore_analysis')
df_thresholds = xl.parse('thresholds')

# --- CONFIGURATION: Adjust these based on your 'thresholds' sheet structure ---
# Assuming 'thresholds' has Trigger in Row 0 and Exit in Row 1
# Column 1 (B) for Phase 1, Column 2 (C) for Phase 2
p1_trigger = df_thresholds.iloc[0, 1]
p1_exit = df_thresholds.iloc[1, 1]

p2_trigger = df_thresholds.iloc[0, 2]
p2_exit = df_thresholds.iloc[1, 2]
# ------------------------------------------------------------------------------

def calculate_payout(value, trigger, exit_val):
    """Applies the formula: (Trigger - Value) / (Trigger - Exit)"""
    # Calculate raw payout
    payout = (trigger - value) / (trigger - exit_val)
    
    # Clip values between 0 and 1
    # This handles the "no negative payout" and "cap at 100%" rules
    return np.clip(payout, 0, 1)

# Create the new Payout DataFrame
df_payout = pd.DataFrame()
df_payout['Year'] = df_zscore['Year']

# Calculate Payouts using the Z-Score columns (D and E from your image)
df_payout['Payout_P1'] = df_zscore['P1_Zscore'].apply(
    lambda x: calculate_payout(x, p1_trigger, p1_exit)
)

df_payout['Payout_P2'] = df_zscore['P2_Zscore'].apply(
    lambda x: calculate_payout(x, p2_trigger, p2_exit)
)

# Save to a new Excel file
output_file = 'Payout_Results.xlsx'
df_payout.to_excel(output_file, index=False)

print(f"Success! Payouts calculated and saved to {output_file}")