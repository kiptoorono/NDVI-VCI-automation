import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import beta, gamma, weibull_min, norm, lognorm, kstest
import warnings
warnings.filterwarnings('ignore')

# Your data
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

# Parse data
lines = data_str.strip().split('\n')
headers = lines[0].split('\t')
data = []
for line in lines[1:]:
    data.append([float(x) for x in line.split('\t')])

df = pd.DataFrame(data, columns=headers)

# Function to fit distributions and calculate goodness-of-fit metrics
def fit_and_test_distributions(data_series, name):
    """Fit multiple distributions and return metrics"""
    
    results = {}
    
    # 1. Beta distribution
    try:
        params_beta = beta.fit(data_series)
        ks_beta = kstest(data_series, lambda x: beta.cdf(x, *params_beta))[1]
        results['Beta'] = {
            'params': params_beta,
            'ks_pvalue': ks_beta,
            'ks_stat': kstest(data_series, lambda x: beta.cdf(x, *params_beta))[0]
        }
    except:
        results['Beta'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    # 2. Gamma distribution
    try:
        params_gamma = gamma.fit(data_series)
        ks_gamma = kstest(data_series, lambda x: gamma.cdf(x, *params_gamma))[1]
        results['Gamma'] = {
            'params': params_gamma,
            'ks_pvalue': ks_gamma,
            'ks_stat': kstest(data_series, lambda x: gamma.cdf(x, *params_gamma))[0]
        }
    except:
        results['Gamma'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    # 3. Weibull distribution
    try:
        params_weibull = weibull_min.fit(data_series)
        ks_weibull = kstest(data_series, lambda x: weibull_min.cdf(x, *params_weibull))[1]
        results['Weibull'] = {
            'params': params_weibull,
            'ks_pvalue': ks_weibull,
            'ks_stat': kstest(data_series, lambda x: weibull_min.cdf(x, *params_weibull))[0]
        }
    except:
        results['Weibull'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    # 4. Lognormal distribution
    try:
        params_lognorm = lognorm.fit(data_series)
        ks_lognorm = kstest(data_series, lambda x: lognorm.cdf(x, *params_lognorm))[1]
        results['Lognormal'] = {
            'params': params_lognorm,
            'ks_pvalue': ks_lognorm,
            'ks_stat': kstest(data_series, lambda x: lognorm.cdf(x, *params_lognorm))[0]
        }
    except:
        results['Lognormal'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    # 5. Normal distribution
    try:
        params_norm = norm.fit(data_series)
        ks_norm = kstest(data_series, lambda x: norm.cdf(x, *params_norm))[1]
        results['Normal'] = {
            'params': params_norm,
            'ks_pvalue': ks_norm,
            'ks_stat': kstest(data_series, lambda x: norm.cdf(x, *params_norm))[0]
        }
    except:
        results['Normal'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    return results

# Fit distributions for all 4 series
print("\n" + "=" * 70)
print("GOODNESS-OF-FIT TESTS (Kolmogorov-Smirnov)")
print("=" * 70)
print("Higher p-value = better fit. p-value > 0.05 suggests good fit.\n")

all_results = {}
best_dist = {}

for col in df.columns:
    all_results[col] = fit_and_test_distributions(df[col].values, col)
    
    print(f"\n{col}:")
    print("-" * 70)
    
    # Sort by KS p-value (higher is better)
    sorted_by_ks = sorted(all_results[col].items(), 
                        key=lambda x: x[1]['ks_pvalue'], 
                        reverse=True)
    
    best_dist[col] = sorted_by_ks[0][0]
    
    for dist_name, metrics in sorted_by_ks:
        if metrics['params'] is not None:
            print(f"  {dist_name:12} | KS p-value: {metrics['ks_pvalue']:.4f} | KS stat: {metrics['ks_stat']:.4f}")
        else:
            print(f"  {dist_name:12} | FAILED TO FIT")

print("\n" + "=" * 70)
print("RECOMMENDED DISTRIBUTIONS:")
print("=" * 70)
for col, dist in best_dist.items():
    p_val = all_results[col][dist]['ks_pvalue']
    print(f"{col:15} → {dist:12} (p-value: {p_val:.4f})")   




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import beta, gamma, weibull_min, norm, lognorm, kstest
import warnings
warnings.filterwarnings('ignore')

# Your data
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

# Parse data
lines = data_str.strip().split('\n')
headers = lines[0].split('\t')
data = []
for line in lines[1:]:
    data.append([float(x) for x in line.split('\t')])

df = pd.DataFrame(data, columns=headers)

# Function to fit distributions
def fit_and_test_distributions(data_series):
    results = {}
    
    try:
        params_beta = beta.fit(data_series)
        ks_beta = kstest(data_series, lambda x: beta.cdf(x, *params_beta))[1]
        results['Beta'] = {'params': params_beta, 'ks_pvalue': ks_beta, 'ks_stat': kstest(data_series, lambda x: beta.cdf(x, *params_beta))[0]}
    except:
        results['Beta'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    try:
        params_gamma = gamma.fit(data_series)
        ks_gamma = kstest(data_series, lambda x: gamma.cdf(x, *params_gamma))[1]
        results['Gamma'] = {'params': params_gamma, 'ks_pvalue': ks_gamma, 'ks_stat': kstest(data_series, lambda x: gamma.cdf(x, *params_gamma))[0]}
    except:
        results['Gamma'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    try:
        params_weibull = weibull_min.fit(data_series)
        ks_weibull = kstest(data_series, lambda x: weibull_min.cdf(x, *params_weibull))[1]
        results['Weibull'] = {'params': params_weibull, 'ks_pvalue': ks_weibull, 'ks_stat': kstest(data_series, lambda x: weibull_min.cdf(x, *params_weibull))[0]}
    except:
        results['Weibull'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    try:
        params_lognorm = lognorm.fit(data_series)
        ks_lognorm = kstest(data_series, lambda x: lognorm.cdf(x, *params_lognorm))[1]
        results['Lognormal'] = {'params': params_lognorm, 'ks_pvalue': ks_lognorm, 'ks_stat': kstest(data_series, lambda x: lognorm.cdf(x, *params_lognorm))[0]}
    except:
        results['Lognormal'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    try:
        params_norm = norm.fit(data_series)
        ks_norm = kstest(data_series, lambda x: norm.cdf(x, *params_norm))[1]
        results['Normal'] = {'params': params_norm, 'ks_pvalue': ks_norm, 'ks_stat': kstest(data_series, lambda x: norm.cdf(x, *params_norm))[0]}
    except:
        results['Normal'] = {'params': None, 'ks_pvalue': 0, 'ks_stat': np.nan}
    
    return results

# Fit all
all_results = {}
for col in df.columns:
    all_results[col] = fit_and_test_distributions(df[col].values)

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

col_names = ['LR_P1_VCI', 'LR_P2_VCI', 'SR_P1_VCI', 'SR_P2_VCI']
best_dists = ['Weibull', 'Weibull', 'Normal', 'Normal']

for idx, (col, best_dist) in enumerate(zip(col_names, best_dists)):
    ax = axes[idx]
    data_vals = df[col].values
    
    ax.hist(data_vals, bins=8, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Data')
    
    params = all_results[col][best_dist]['params']
    x = np.linspace(data_vals.min() - 0.05, data_vals.max() + 0.05, 200)
    
    if best_dist == 'Weibull':
        y = weibull_min.pdf(x, *params)
    elif best_dist == 'Normal':
        y = norm.pdf(x, *params)
    elif best_dist == 'Gamma':
        y = gamma.pdf(x, *params)
    elif best_dist == 'Lognormal':
        y = lognorm.pdf(x, *params)
    elif best_dist == 'Beta':
        y = beta.pdf(x, *params)
    
    ax.plot(x, y, 'r-', linewidth=2.5, label=f'{best_dist} fit')
    
    p_val = all_results[col][best_dist]['ks_pvalue']
    ax.set_title(f'{col}\n{best_dist} (p-value: {p_val:.4f})', fontsize=11, fontweight='bold')
    ax.set_xlabel('VCI Value', fontsize=10)
    ax.set_ylabel('Density', fontsize=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('vci_distribution_fits.png', dpi=100, bbox_inches='tight')
plt.show()

print("Distribution fit visualization created!")
