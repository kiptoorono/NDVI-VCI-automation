# ◈ NDVI / VCI Insurance Risk Automation

> Index-based agricultural risk monitoring and payout automation for underwriting, claims support, and drought stress assessment.

## ◌ Project Purpose

This repository processes agricultural and climate data to monitor seasonal stress conditions and translate them into insurance-style indicators. The code reads workbook-based NDVI, rainfall, and vegetation-condition data, summarizes seasonal patterns, calculates stress thresholds, and produces payout-style outputs for underwriting and parametric insurance use cases.

In practical terms, the project is designed to answer questions such as:

- Is a region experiencing abnormal vegetation stress?
- Has rainfall or vegetation fallen below a defined trigger threshold for a season?
- What payout exposure would a drought or stress event generate under an index-based insurance model?
- How does the risk profile change under simulated tail-risk scenarios?

---

## ◍ Underwriting and Insurance Lens

The repository is designed around index insurance logic rather than claim-by-claim loss adjustment. Instead of relying on individual farm damage assessments, it uses satellite and climate indicators to model regional agricultural stress and convert that into a normalized risk signal.

The core operating flow is:

1. Aggregate dekadal NDVI and rainfall values into seasonal sums.
2. Compare each year against historical behavior using z-scores.
3. Define trigger and exit thresholds for drought or stress conditions.
4. Convert vegetation performance into a VCI signal.
5. Estimate payout exposure using trigger/exit formulas.
6. Run stochastic simulations to understand tail risk and sensitivity.

This follows the logic commonly used in parametric agricultural insurance and climate-index underwriting.

---

## ⟡ What the Code Is Doing

### 1) NDVI seasonal aggregation
Files such as `summation.py` and `z-score.py` read an Excel workbook, select a source sheet, and aggregate NDVI values across fixed dekad windows.

Typical logic:

- phase 1: dekads 9–13
- phase 2: dekads 14–17
- sum values across years
- filter out years beyond 2025
- save outputs in sheets such as `dekad_sums` and `zscore_analysis`

This creates the historical seasonal baseline needed for stress detection.

### 2) Rainfall stress analysis
`New/SPI calculation.py` performs a similar workflow for rainfall data using SPI-style standardized anomalies. It calculates seasonal sums and z-scores for rainfall phases and writes them into workbook sheets such as:

- `dekad_sums`
- `SPI`

This allows rainfall shortfall to be monitored alongside vegetation stress.

### 3) VCI calculation
`New/VCI.py` calculates a Vegetation Condition Index (VCI) for long rainy (LR) and short rainy (SR) seasons by comparing each year’s average NDVI against the observed minimum and maximum range.

The core relationship is:

$VCI = \frac{\overline{NDVI} - NDVI_{min}}{NDVI_{max} - NDVI_{min}}$

This produces a normalized measure of vegetation stress, where values closer to 0 indicate poor conditions and values closer to 1 indicate healthier vegetation conditions.

### 4) Trigger and exit thresholds
`triggers.py` computes z-score thresholds using percentiles:

- trigger = 25th percentile
- exit = 2.5th percentile

These thresholds define when a region crosses a protection or distress point, which is highly relevant for index-based insurance triggers.

### 5) Payout logic
`PAYOUT.PY` replicates the underwriting payout formula used in the workbook model:

$Payout = \min(C, \max(0, \frac{Trigger - Z}{Trigger - Exit}))$

This is intentionally structured like a parametric payout model: values below the trigger produce positive indemnity, values below the exit limit are capped, and healthy values remain at zero.

A real example from the repo is:

- $C_{P1} = \frac{5}{9}$
- $C_{P2} = \frac{4}{9}$

This indicates capped payout exposure by risk phase, which is common in insurance-index structures.

### 6) Stochastic and tail-risk simulation
Files such as `simulation.py`, `gamma.py`, and `New/VCI simulation.py` fit probability distributions to observed outcomes and generate simulated results. The code uses gamma distribution fitting and clips output values to a maximum of 1.0.

This is useful for:

- stress testing the model
- understanding tail event severity
- estimating policy exposure under adverse scenarios
- comparing distributional behavior before and after climate stress

---

## ▣ Repository Structure

```text
.
├── 📊 Combine_UAI_Final_CHIRP_MeanDailyRainfall_final.csv
├── 📊 Combine_UAI_Final_CHIRP_MeanDailyRainfall_final.csv.xlsx
├── 📊 Combine_UAI_Final_NDVI_final.csv
├── 📊 Combine_UAI_Final_NDVI_final.xlsx
├── ⌬ Distribution fit .py
├── ⌁ PAYOUT.PY
├── ◫ gamma.py
├── ◫ simulation.py
├── ◫ summation.py
├── ◫ triggers.py
├── ◫ z-score.py
├── ◫ exe.py
├── ◫ plot.py
├── ⟡ tail_stretching Simulation.py
├── ◌ tail_inflation_comparison.png
├── ◌ gamma_assessment.png
├── ◌ gamma_assessment_comparison.png
├── ◌ vci_distribution_fits.png
├── ▭ New/
│   ├── SPI calculation.py
│   ├── SPI simulation.py
│   ├── VCI.py
│   ├── VCI simulation.py
│   ├── VCI simulation tail blowout.py
│   └── standadise SPI.py
├── ▭ bundle/
└── .gitignore
```

---

## ◈ Main Files and Their Role

- `summation.py` — aggregates NDVI dekad totals by phase.
- `z-score.py` — computes z-score-based stress analysis for NDVI.
- `triggers.py` — derives trigger and exit threshold values.
- `PAYOUT.PY` — calculates index-based payout based on z-score thresholds.
- `simulation.py` — simulates payout results using gamma parameters.
- `New/VCI.py` — calculates VCI values by season and year.
- `New/SPI calculation.py` — processes rainfall and SPI-style standardized values.
- `exe.py` — Tkinter-based desktop workflow for running the pipeline in Excel.
- `gamma.py` — visualizes distribution behavior before and after clipping.

---

## ⌘ Typical Pipeline

```text
Input workbook (NDVI / rainfall Excel data)
        ↓
Summarize seasonal dekads
        ↓
Normalize using z-scores / SPI-like analysis
        ↓
Compute trigger and exit thresholds
        ↓
Calculate VCI and seasonal stress measures
        ↓
Generate payout values
        ↓
Simulate outcomes and store results in workbook sheets
```

This is a classic underwriting workflow for index-based protection products: signal extraction → thresholding → payout estimation → risk simulation.

---

## ⎍ Output Sheets Produced by the Workflow

The scripts create or overwrite workbook sheets such as:

- `dekad_sums`
- `zscore_analysis`
- `thresholds`
- `payout`
- `simulation_results`
- `VCI`
- `VCI_Parameters`
- `VCI_Simulations`

These outputs are designed to be consumed in Excel-based underwriting review, analysis, and reporting.

---

## ✦ Stack and Dependencies

This project is a Python-based analytics toolkit.

Primary libraries used:

- `numpy`
- `pandas`
- `openpyxl`
- `scipy`
- `matplotlib`
- `tkinter`

This makes it a spreadsheet-driven analytical environment rather than a web app or API service.

---

## ▶ How to Run

### Install requirements

```bash
pip install numpy pandas openpyxl scipy matplotlib
```

### Run the core pipeline manually

```bash
python summation.py
python z-score.py
python triggers.py
python PAYOUT.PY
```

### Run the VCI / SPI analysis

```bash
python "New/SPI calculation.py"
python "New/VCI.py"
python "New/VCI simulation.py"
```

### Launch the desktop UI

```bash
python exe.py
```

This opens a simple Tkinter-based dashboard that allows the user to select an Excel workbook and run the underwriting pipeline steps.

---

## ⚑ Important Notes

- This repository is not a production SaaS platform; it is a workbook-driven data science and underwriting analysis toolkit.
- Many scripts use hard-coded Windows-style paths and workbook names.
- The project is oriented around Excel input/output rather than database-backed processing.
- The risk logic is designed for index-based agricultural insurance and drought monitoring scenarios.

---

## ✓ Summary

This repository is an analytical underwriting engine for agricultural risk based on satellite-based vegetation and rainfall indicators. It transforms raw climate and NDVI data into seasonal stress metrics, calculates trigger/exit thresholds, estimates index payouts, and simulates tail risk to support insurance decision-making and exposure analysis.

It sits squarely in the world of parametric agricultural insurance, climate risk underwriting, and disaster-index modeling.

---

## ◬ Suggested Project Tagline

Satellite-driven agricultural risk analytics for index insurance underwriting.

