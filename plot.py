
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_NDVI_final.xlsx"

# Read both sheets
df_original = pd.read_excel(path, sheet_name='VCI_Simulations')
df_blowout = pd.read_excel(path, sheet_name='VCI_Simulations_blowout')

# Columns to plot
cols = ['LR_P1_VCI', 'LR_P2_VCI']

# Create a 2x2 subplot figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Distribution Comparison: Original vs Blowout Simulations', fontsize=16, fontweight='bold')

# Plot histograms + KDE for each column
for idx, col in enumerate(cols):
    # Original simulations
    ax1 = axes[idx, 0]
    ax1.hist(df_original[col], bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    ax1.set_title(f'{col} - Original Simulations', fontweight='bold')
    ax1.set_xlabel('Value')
    ax1.set_ylabel('Frequency')
    ax1.grid(alpha=0.3)
    
    # Add statistics
    mean_orig = df_original[col].mean()
    std_orig = df_original[col].std()
    ax1.axvline(mean_orig, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_orig:.4f}')
    ax1.legend()
    
    # Blowout simulations
    ax2 = axes[idx, 1]
    ax2.hist(df_blowout[col], bins=50, alpha=0.7, color='coral', edgecolor='black')
    ax2.set_title(f'{col} - Blowout Simulations', fontweight='bold')
    ax2.set_xlabel('Value')
    ax2.set_ylabel('Frequency')
    ax2.grid(alpha=0.3)
    
    # Add statistics
    mean_blowout = df_blowout[col].mean()
    std_blowout = df_blowout[col].std()
    ax2.axvline(mean_blowout, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_blowout:.4f}')
    ax2.legend()

plt.tight_layout()
plt.show()

# Print summary statistics
print("=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)
for col in cols:
    print(f"\n{col}:")
    print(f"  Original Simulations:")
    print(f"    Mean: {df_original[col].mean():.6f}")
    print(f"    Std Dev: {df_original[col].std():.6f}")
    print(f"    Min: {df_original[col].min():.6f}")
    print(f"    Max: {df_original[col].max():.6f}")
    print(f"  Blowout Simulations:")
    print(f"    Mean: {df_blowout[col].mean():.6f}")
    print(f"    Std Dev: {df_blowout[col].std():.6f}")
    print(f"    Min: {df_blowout[col].min():.6f}")
    print(f"    Max: {df_blowout[col].max():.6f}")