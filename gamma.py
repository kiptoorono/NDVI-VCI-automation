import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# GAMMA DISTRIBUTION VISUALIZATION CODE - FIXED LAYOUT (NO OVERLAPS)
# ============================================================================

# Your parameters
shape1, scale1 = 0.2423, 0.3606
shape2, scale2 = 0.2209, 0.2841

# Generate samples
n_samples = 10000
sim1 = np.random.gamma(shape1, scale1, n_samples)
sim2 = np.random.gamma(shape2, scale2, n_samples)

# Clip
sim1_clipped = np.clip(sim1, 0, 1.0)
sim2_clipped = np.clip(sim2, 0, 1.0)

clipped_pct1 = (sim1 >= 1.0).sum() / n_samples * 100
clipped_pct2 = (sim2 >= 1.0).sum() / n_samples * 100

# Create figure with more vertical space between rows
fig = plt.figure(figsize=(16, 14))
gs = fig.add_gridspec(3, 2, hspace=0.55, wspace=0.3,
                      top=0.91, bottom=0.04, left=0.07, right=0.97)

def style_hist(ax, title):
    # Place title below the axes top to avoid suptitle collision
    ax.set_title(title, fontweight='bold', fontsize=11, pad=8, loc='center')
    ax.set_xlabel('Value', fontsize=10)
    ax.set_ylabel('Density', fontsize=10)
    ax.grid(alpha=0.3, linestyle='--')
    ax.legend(loc='upper right', fontsize=9, framealpha=0.8)

# ========== P1 RAW ==========
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(sim1, bins=150, density=True, alpha=0.75, color='steelblue',
         edgecolor='black', linewidth=0.5)
ax1.axvline(np.mean(sim1), color='red', linestyle='--', linewidth=2.5,
            label=f'Mean = {np.mean(sim1):.4f}')
ax1.axvline(np.median(sim1), color='green', linestyle=':', linewidth=2,
            label=f'Median = {np.median(sim1):.4f}')
ax1.set_xlim(0, 1.2)
style_hist(ax1, 'P1: Raw Gamma Distribution (Unclipped)')
# Move params box to lower right to avoid legend overlap
ax1.text(0.97, 0.55, f'Shape = {shape1:.4f}\nScale = {scale1:.4f}',
         transform=ax1.transAxes, ha='right', va='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6), fontsize=9)

# ========== P1 CLIPPED ==========
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(sim1_clipped, bins=150, density=True, alpha=0.75, color='coral',
         edgecolor='black', linewidth=0.5)
ax2.axvline(np.mean(sim1_clipped), color='red', linestyle='--', linewidth=2.5,
            label=f'Mean = {np.mean(sim1_clipped):.4f}')
ax2.axvline(np.median(sim1_clipped), color='green', linestyle=':', linewidth=2,
            label=f'Median = {np.median(sim1_clipped):.4f}')
ax2.axvline(1.0, color='purple', linestyle='-', linewidth=2, alpha=0.6,
            label='Cap at 1.0')
ax2.set_xlim(-0.05, 1.05)
style_hist(ax2, 'P1: After Clipping to [0, 1]')
ax2.text(0.60, 0.55, f'{clipped_pct1:.3f}% values\nexceeded cap',
         transform=ax2.transAxes, ha='center', va='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8), fontsize=9)

# ========== P2 RAW ==========
ax3 = fig.add_subplot(gs[1, 0])
ax3.hist(sim2, bins=150, density=True, alpha=0.75, color='steelblue',
         edgecolor='black', linewidth=0.5)
ax3.axvline(np.mean(sim2), color='red', linestyle='--', linewidth=2.5,
            label=f'Mean = {np.mean(sim2):.4f}')
ax3.axvline(np.median(sim2), color='green', linestyle=':', linewidth=2,
            label=f'Median = {np.median(sim2):.4f}')
ax3.set_xlim(0, 0.8)
style_hist(ax3, 'P2: Raw Gamma Distribution (Unclipped)')
ax3.text(0.97, 0.55, f'Shape = {shape2:.4f}\nScale = {scale2:.4f}',
         transform=ax3.transAxes, ha='right', va='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6), fontsize=9)

# ========== P2 CLIPPED ==========
ax4 = fig.add_subplot(gs[1, 1])
ax4.hist(sim2_clipped, bins=150, density=True, alpha=0.75, color='coral',
         edgecolor='black', linewidth=0.5)
ax4.axvline(np.mean(sim2_clipped), color='red', linestyle='--', linewidth=2.5,
            label=f'Mean = {np.mean(sim2_clipped):.4f}')
ax4.axvline(np.median(sim2_clipped), color='green', linestyle=':', linewidth=2,
            label=f'Median = {np.median(sim2_clipped):.4f}')
ax4.axvline(1.0, color='purple', linestyle='-', linewidth=2, alpha=0.6,
            label='Cap at 1.0')
ax4.set_xlim(-0.05, 1.05)
style_hist(ax4, 'P2: After Clipping to [0, 1]')
ax4.text(0.60, 0.55, f'{clipped_pct2:.3f}% values\nexceeded cap',
         transform=ax4.transAxes, ha='center', va='center',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8), fontsize=9)

# ========== SUMMARY TABLE ==========
ax5 = fig.add_subplot(gs[2, :])
ax5.axis('off')

summary_data = [
    ['Metric', 'P1 Raw', 'P1 Clipped', 'P2 Raw', 'P2 Clipped'],
    ['Mean',    f'{np.mean(sim1):.6f}',   f'{np.mean(sim1_clipped):.6f}',   f'{np.mean(sim2):.6f}',   f'{np.mean(sim2_clipped):.6f}'],
    ['Std Dev', f'{np.std(sim1):.6f}',    f'{np.std(sim1_clipped):.6f}',    f'{np.std(sim2):.6f}',    f'{np.std(sim2_clipped):.6f}'],
    ['Median',  f'{np.median(sim1):.6f}', f'{np.median(sim1_clipped):.6f}', f'{np.median(sim2):.6f}', f'{np.median(sim2_clipped):.6f}'],
    ['Min',     f'{np.min(sim1):.6f}',    f'{np.min(sim1_clipped):.6f}',    f'{np.min(sim2):.6f}',    f'{np.min(sim2_clipped):.6f}'],
    ['Max',     f'{np.max(sim1):.6f}',    '1.000000',                        f'{np.max(sim2):.6f}',    '1.000000'],
    ['% ≥ 1.0', f'{clipped_pct1:.4f}%',  'N/A',                             f'{clipped_pct2:.4f}%',   'N/A'],
]

ax5.text(0.5, 0.97, 'Summary Statistics (10,000 samples)',
         ha='center', va='top', fontsize=13, fontweight='bold',
         transform=ax5.transAxes)

table = ax5.table(cellText=summary_data, cellLoc='center', loc='center',
                  colWidths=[0.15, 0.18, 0.18, 0.18, 0.18],
                  bbox=[0.05, 0.0, 0.9, 0.82])

table.auto_set_font_size(False)
table.set_fontsize(10)

for i in range(5):
    table[(0, i)].set_facecolor('#4472C4')
    table[(0, i)].set_text_props(weight='bold', color='white')

for i in range(1, len(summary_data)):
    for j in range(5):
        facecolor = '#E7E6E6' if i % 2 == 0 else '#F2F2F2'
        table[(i, j)].set_facecolor(facecolor)

# Main title - well above all subplots
plt.suptitle('Gamma Distribution Assessment — P1 and P2 Simulations',
             fontsize=15, fontweight='bold', y=0.975)

plt.savefig('gamma_assessment.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved to gamma_assessment.png")