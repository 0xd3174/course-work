import numpy as np

def calculate_bge_ph():
    print("--- Theoretical pH calculation of Background Electrolyte (BGE) ---")
    # Constants
    Kw = 1e-14
    # pKa values (at 20-25 °C)
    # Chromic acid H2CrO4: pKa1 is very low (~ -0.7, fully dissociated to HCrO4-). pKa2 = 6.50
    pKa2_cr = 6.50
    Ka2_cr = 10**(-pKa2_cr)
    
    # Diethanolamine (DEA): pKa of BH+ is ~ 8.88 at 25 °C, ~ 9.00 at 20 °C
    # Let's use pKa_dea = 8.88
    pKa_dea = 8.88
    Ka_dea = 10**(-pKa_dea)
    
    # Concentrations in M
    C_cr = 0.010    # 10 mmol/L CrO3
    C_dea = 0.030   # 30 mmol/L DEA
    C_cta = 0.002   # 2 mmol/L CTA-OH (fully dissociated strong base)
    
    # We solve for [H+] using the charge balance equation:
    # [H+] + [CTA+] + [BH+] = [OH-] + [HCrO4-] + 2[CrO4^2-]
    # [CTA+] = C_cta = 0.002 M
    # [BH+] = C_dea * [H+] / ([H+] + Ka_dea)
    # [OH-] = Kw / [H+]
    # [CrO4^2-] = C_cr * Ka2_cr / ([H+] + Ka2_cr)
    # [HCrO4-] = C_cr * [H+] / ([H+] + Ka2_cr)
    
    # Let's solve numerically for pH in range 5 to 11
    ph_range = np.linspace(5, 11, 100000)
    best_ph = None
    min_diff = float('inf')
    
    for ph in ph_range:
        h = 10**(-ph)
        oh = Kw / h
        
        # Species
        cta = C_cta
        bh = C_dea * h / (h + Ka_dea)
        
        # Chromate species
        hcro4 = C_cr * h / (h + Ka2_cr)
        cro4 = C_cr * Ka2_cr / (h + Ka2_cr)
        
        # Charge balance
        lhs = h + cta + bh
        rhs = oh + hcro4 + 2 * cro4
        
        diff = abs(lhs - rhs)
        if diff < min_diff:
            min_diff = diff
            best_ph = ph
            
    print(f"Calculated BGE pH (using pKa_DEA = 8.88): {best_ph:.3f}")
    
    # At 20 °C, the pKa of amines increases. Let's recalculate for pKa_DEA = 9.00
    pKa_dea_20 = 9.00
    Ka_dea_20 = 10**(-pKa_dea_20)
    
    min_diff_20 = float('inf')
    best_ph_20 = None
    for ph in ph_range:
        h = 10**(-ph)
        oh = Kw / h
        cta = C_cta
        bh = C_dea * h / (h + Ka_dea_20)
        hcro4 = C_cr * h / (h + Ka2_cr)
        cro4 = C_cr * Ka2_cr / (h + Ka2_cr)
        
        lhs = h + cta + bh
        rhs = oh + hcro4 + 2 * cro4
        
        diff = abs(lhs - rhs)
        if diff < min_diff_20:
            min_diff_20 = diff
            best_ph_20 = ph
            
    print(f"Calculated BGE pH (using pKa_DEA = 9.00 at 20 °C): {best_ph_20:.3f}")
    return best_ph, best_ph_20

def analyze_experimental_data():
    print("\n--- Experimental Data Analysis for Real Samples ---")
    # Data from 'галя' images:
    # Anions: Chloride, Nitrite, Sulfate, Nitrate, Phosphate
    # (Fluoride is not detected in these samples, let's keep it as ND)
    
    # Samples: галя а1, а4, а5, а6, а7, а9
    # Concentrations in mg/dm3
    data = {
        'Chloride': [25.81, 14.76, 19.59, 21.40, 17.46, 54.38],
        'Nitrite': [0.0, 0.0, 0.03776, 0.02384, 0.0, 0.0],  # 0.0 means not detected (below LOD/LOQ)
        'Sulfate': [30.89, 24.83, 31.38, 33.10, 27.64, 29.25],
        'Nitrate': [1.382, 0.7873, 0.8426, 1.071, 1.221, 0.8494],
        'Phosphate': [0.4230, 0.4585, 0.4257, 0.4372, 0.4220, 0.3438]
    }
    
    # Let's calculate mean, SD, and RSD for each anion
    # We exclude 0.0 values from calculations for Nitrite, as it is mostly not detected
    # We will treat Nitrite as < LOQ except for а5 and а6.
    # Wait, is а9 a special sample (with Chloride = 54.38)? Let's check RSDs.
    
    for anion, values in data.items():
        arr = np.array(values)
        if anion == 'Nitrite':
            detected = arr[arr > 0]
            if len(detected) > 0:
                mean = np.mean(detected)
                sd = np.std(detected, ddof=1) if len(detected) > 1 else 0.0
                rsd = (sd / mean) * 100 if mean > 0 else 0.0
                print(f"{anion}: detected in {len(detected)}/6 samples. Mean of detected: {mean:.4f} mg/dm3, SD: {sd:.4f}, RSD: {rsd:.1f}%")
            else:
                print(f"{anion}: Not detected (< LOQ)")
        else:
            mean = np.mean(arr)
            sd = np.std(arr, ddof=1)
            rsd = (sd / mean) * 100
            print(f"{anion}: Mean: {mean:.3f} mg/dm3, SD: {sd:.3f}, RSD: {rsd:.1f}%, Min: {np.min(arr):.3f}, Max: {np.max(arr):.3f}")

if __name__ == '__main__':
    calculate_bge_ph()
    analyze_experimental_data()
