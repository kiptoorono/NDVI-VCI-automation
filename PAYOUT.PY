"""
Exact hard-coded copy of the payout logic from PAYOUT.PY,
with no config imports and a fixed workbook path.
"""

from typing import List

import openpyxl


def _payout_from_z(value: float, trigger: float, exit_: float, cap: float) -> float:
    """Replicate the Excel formula:

    =MIN(cap, MAX(0, (trigger - value) / (trigger - exit)))
    """
    if trigger == exit_:
        return 0.0
    raw = (trigger - value) / (trigger - exit_)
    return float(min(cap, max(0.0, raw)))


def run_hardcoded_payout():
    # Hard-coded workbook path and sheet names
    workbook_path = r"C:\Users\Rono\Desktop\Excel workbook automation\Combine_UAI_Final_NDVI_final.xlsx"
    zscore_sheet = "zscore_analysis"
    payout_sheet = "payout"
    thresholds_sheet = "thresholds"

    wb = openpyxl.load_workbook(workbook_path, data_only=True)

    if zscore_sheet not in wb.sheetnames:
        raise ValueError(f"Z-score sheet '{zscore_sheet}' not found in workbook.")
    if thresholds_sheet not in wb.sheetnames:
        raise ValueError(f"Thresholds sheet '{thresholds_sheet}' not found in workbook.")

    ws_z = wb[zscore_sheet]
    ws_t = wb[thresholds_sheet]

    # Thresholds layout:
    # Row 1: ["Metric", "Value", "", "Metric", "Value"]
    # Row 2: ["trigger_p1", p1_trigger, "", "exit_p1", p1_exit]
    # Row 3: ["trigger_p2", p2_trigger, "", "exit_p2", p2_exit]
    trigger_p1 = float(ws_t["B2"].value)
    exit_p1 = float(ws_t["E2"].value)
    trigger_p2 = float(ws_t["B3"].value)
    exit_p2 = float(ws_t["E3"].value)

    years: List = []
    p1_z_list: List[float] = []
    p2_z_list: List[float] = []

    # Read z-scores from zscore_analysis (skip header and summary rows)
    # Expected structure matches PAYOUT.PY:
    # - Column A: Year
    # - Column D: Phase1_Zscore
    # - Column E: Phase2_Zscore
    for row in ws_z.iter_rows(min_row=2, values_only=True):
        year, _, _, p1_z, p2_z = row[:5]
        if year is None and p1_z is None and p2_z is None:
            break
        years.append(year)
        p1_z_list.append(float(p1_z if p1_z is not None else 0.0))
        p2_z_list.append(float(p2_z if p2_z is not None else 0.0))

    # Create / replace payout sheet
    if payout_sheet in wb.sheetnames:
        del wb[payout_sheet]
    ws_payout = wb.create_sheet(payout_sheet)

    # Only keep required columns in the payout sheet
    ws_payout.append(
        [
            "Year",
            "Payout_P1",
            "Payout_P2",
        ]
    )

    # Phase-specific caps, matching your Excel:
    # Payout_P1: MIN(5/9, MAX(0, (trigger_p1 - z1)/(trigger_p1 - exit_p1)))
    # Payout_P2: MIN(4/9, MAX(0, (trigger_p2 - z2)/(trigger_p2 - exit_p2)))
    cap_p1 = 5.0 / 9.0
    cap_p2 = 4.0 / 9.0

    for i, year in enumerate(years):
        z1 = p1_z_list[i]
        z2 = p2_z_list[i]
        payout1 = _payout_from_z(z1, trigger_p1, exit_p1, cap_p1)
        payout2 = _payout_from_z(z2, trigger_p2, exit_p2, cap_p2)
        ws_payout.append(
            [
                year,
                payout1,
                payout2,
            ]
        )

    wb.save(workbook_path)
    print("Hard-coded payout calculation complete.")


if __name__ == "__main__":
    run_hardcoded_payout()

