
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gamma, skew, kurtosis
from io import StringIO

# Recreate the data and simulations
data_str = """LR_P1_VCI	LR_P2_VCI	SR_P1_VCI	SR_P2_VCI
0.2785	0.3477	0.4541	0.5398
0.161	0.1747	0.3242	0.4196
0.1394	0.1591	0.2961	0.2014
0.1566	0.139	0.3188	0.6705
0.256	0.2619	0.5055	0.5089
0.3978	0.3315	0.406	0.3963
0.1412	0.1363	0.2952	0.4347
0.4776	0.3163	0.3249	0.2172
0.0424	0.0284	0.3039	0.5874
0.1181	0.1527	0.1842	0.4237
0.604	0.4246	0.3344	0.388
0.4288	0.3114	0.2298	0.4249
0.4716	0.4514	0.3807	0.5054
0.1921	0.2402	0.2236	0.2683
0.1255	0.189	0.1566	0.2325
0.6854	0.7655	0.5892	0.3036
0.0825	0.17	0.2169	0.7061
0.6356	0.6776	0.5534	0.513
0.2411	0.1244	0.1311	0.2454
0.1101	0.1529	0.0971	0.2682
0.385	0.4987	0.1902	0.5382
0.5562	0.531	0.3916	0.4122
0.5538	0.3846	0.1855	0.2844"""

df = pd.read_csv(StringIO(data_str), sep='\t')
vci_cols = df.columns.tolist()
epsilon = 1e-9
num_simulations = 10000

# Generate simulations
simulation_data = {}
np.random.seed(123)
for col in vci_cols:
    data = df[col].dropna().values
    data = np.where(data <= 0, epsilon, data)
    fitted_distribution = gamma.fit(data)
    simulated_data_raw = gamma.rvs(*fitted_distribution, size=num_simulations)
    simulation_data[col] = np.minimum(simulated_data_raw, 1)

# Get thresholds
thresholds = {}
for col in vci_cols:
    thresholds[col] = np.percentile(simulation_data[col], 90)

print("Distribution Analysis: Before vs After Stressing")
print("=" * 100)

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 14))
gs = fig.add_gridspec(4, 4, hspace=0.35, wspace=0.3)

# stress factor to analyze
main_stress = 1.25

for idx, col in enumerate(vci_cols):
    original = simulation_data[col].copy()
    threshold = thresholds[col]
    
    # Apply  sigmoid stress
    stressed = original.copy()
    tail_mask = original >= threshold
    tail_vals = original[tail_mask]
    distance_to_1 = 1.0 - tail_vals
    compressed = 1.0 - (distance_to_1 / main_stress)
    stressed[tail_mask] = np.minimum(compressed, 1.0)
    
    # Row 1-3: Histograms + KDE
    ax_hist = fig.add_subplot(gs[0:3, idx])
    
    # Plot both histograms
    bins = 50
    ax_hist.hist(original, bins=bins, alpha=0.5, label='Original', color='blue', density=True, edgecolor='black', linewidth=0.5)
    ax_hist.hist(stressed, bins=bins, alpha=0.5, label=f'Stressed (σ={main_stress})', color='red', density=True, edgecolor='black', linewidth=0.5)
    
    # Add KDE lines
    from scipy.stats import gaussian_kde
    kde_orig = gaussian_kde(original)
    kde_stress = gaussian_kde(stressed)
    x_range = np.linspace(0, 1, 200)
    ax_hist.plot(x_range, kde_orig(x_range), 'b-', linewidth=2.5, label='KDE Original')
    ax_hist.plot(x_range, kde_stress(x_range), 'r-', linewidth=2.5, label='KDE Stressed')
    
    # Mark threshold
    ax_hist.axvline(threshold, color='green', linestyle='--', linewidth=2, alpha=0.7, label=f'90th %ile ({threshold:.3f})')
    
    ax_hist.set_title(f'{col}\n(Threshold: {threshold:.4f})', fontsize=11, fontweight='bold')
    ax_hist.set_xlabel('VCI Value', fontsize=10)
    ax_hist.set_ylabel('Density', fontsize=10)
    ax_hist.legend(fontsize=8, loc='upper left')
    ax_hist.grid(True, alpha=0.3)
    ax_hist.set_xlim(-0.05, 1.05)
    
    # Statistics table
    ax_stats = fig.add_subplot(gs[3, idx])
    ax_stats.axis('off')
    
    # Calculate statistics
    stats_orig = {
        'Mean': np.mean(original),
        'Std': np.std(original),
        'Skew': skew(original),
        'Kurt': kurtosis(original),
        'Min': np.min(original),
        'Max': np.max(original),
        'Tail Mean': np.mean(original[tail_mask]),
        'Tail %': np.sum(tail_mask) / len(original) * 100,
    }
    
    stats_stress = {
        'Mean': np.mean(stressed),
        'Std': np.std(stressed),
        'Skew': skew(stressed),
        'Kurt': kurtosis(stressed),
        'Min': np.min(stressed),
        'Max': np.max(stressed),
        'Tail Mean': np.mean(stressed[tail_mask]),
        'Tail %': np.sum(stressed >= threshold) / len(stressed) * 100,
    }
    
    # Create comparison table
    table_data = []
    table_data.append(['Metric', 'Original', 'Stressed', 'Δ', '% Δ'])
    table_data.append(['-'*15, '-'*12, '-'*12, '-'*10, '-'*10])
    
    for key in stats_orig.keys():
        orig_val = stats_orig[key]
        stress_val = stats_stress[key]
        if key in ['Mean', 'Std', 'Tail Mean']:
            delta = stress_val - orig_val
            pct_delta = (delta / orig_val * 100) if orig_val != 0 else 0
            table_data.append([
                key,
                f'{orig_val:.4f}',
                f'{stress_val:.4f}',
                f'{delta:+.4f}',
                f'{pct_delta:+.2f}%'
            ])
        else:
            table_data.append([
                key,
                f'{orig_val:.2f}',
                f'{stress_val:.2f}',
                f'{stress_val-orig_val:+.2f}',
                ''
            ])
    
    # Format table text
    table_text = '\n'.join([' | '.join(row) for row in table_data])
    
    ax_stats.text(0.05, 0.95, table_text, transform=ax_stats.transAxes,
                  fontsize=8, verticalalignment='top', fontfamily='monospace',
                  bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.2, pad=0.5))

fig.suptitle(f'Distribution Analysis: Original vs Sigmoid-Stressed (σ={main_stress})\nDensity + CDF + Statistics', 
             fontsize=14, fontweight='bold', y=0.995)

plt.savefig('distribution_before_after_stress 1.25.png', dpi=150, bbox_inches='tight')
print("✓ Main distribution comparison saved\n")
plt.show()

# Detailed statistics
print("\n" + "="*100)
print("DETAILED STATISTICS: BEFORE vs AFTER STRESSING")
print("="*100)

for col in vci_cols:
    original = simulation_data[col].copy()
    threshold = thresholds[col]
    
    stressed = original.copy()
    tail_mask = original >= threshold
    tail_vals = original[tail_mask]
    distance_to_1 = 1.0 - tail_vals
    compressed = 1.0 - (distance_to_1 / main_stress)
    stressed[tail_mask] = np.minimum(compressed, 1.0)
    
    print(f"\n{'='*100}")
    print(f"{col.upper()}")
    print(f"{'='*100}")
    
    # Statistics
    stats = {
        'Mean': (np.mean(original), np.mean(stressed)),
        'Median': (np.median(original), np.median(stressed)),
        'Std Dev': (np.std(original), np.std(stressed)),
        'Variance': (np.var(original), np.var(stressed)),
        'Skewness': (skew(original), skew(stressed)),
        'Kurtosis': (kurtosis(original), kurtosis(stressed)),
        'Min': (np.min(original), np.min(stressed)),
        'Max': (np.max(original), np.max(stressed)),
        'Range': (np.max(original) - np.min(original), np.max(stressed) - np.min(stressed)),
        '10th %ile': (np.percentile(original, 10), np.percentile(stressed, 10)),
        '25th %ile': (np.percentile(original, 25), np.percentile(stressed, 25)),
        '50th %ile': (np.percentile(original, 50), np.percentile(stressed, 50)),
        '75th %ile': (np.percentile(original, 75), np.percentile(stressed, 75)),
        '90th %ile': (np.percentile(original, 90), np.percentile(stressed, 90)),
        '95th %ile': (np.percentile(original, 95), np.percentile(stressed, 95)),
        '99th %ile': (np.percentile(original, 99), np.percentile(stressed, 99)),
        'Tail Mean (≥90th)': (np.mean(original[tail_mask]), np.mean(stressed[tail_mask])),
        'Tail Std': (np.std(original[tail_mask]), np.std(stressed[tail_mask])),
        'Values @1.0': (np.sum(original >= 0.9999), np.sum(stressed >= 0.9999)),
    }
    
    print(f"{'Metric':<20} {'Original':>15} {'Stressed':>15} {'Change':>15} {'% Change':>15}")
    print(f"{'-'*82}")
    
    for metric, (orig, stress) in stats.items():
        change = stress - orig
        pct_change = (change / orig * 100) if orig != 0 else 0
        print(f"{metric:<20} {orig:>15.6f} {stress:>15.6f} {change:>+15.6f} {pct_change:>+14.2f}%")