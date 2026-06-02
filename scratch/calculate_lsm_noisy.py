import numpy as np
from scipy import stats

def calculate_lsm_noisy():
    # Set seed for reproducibility
    np.random.seed(12345)
    
    # Calibration target slopes (k in C = k * S)
    targets = {
        'Хлорид':  {'k': 0.1248, 'x': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5])},
        'Нитрит':  {'k': 0.1600, 'x': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2])},
        'Сульфат': {'k': 0.1531, 'x': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5])},
        'Нитрат':  {'k': 0.2004, 'x': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2])},
        'Фторид':  {'k': 0.0445, 'x': np.array([10.0, 10.0, 5.0, 5.0, 1.0, 1.0, 0.1, 0.1])},
        'Фосфат':  {'k': 0.1009, 'x': np.array([25.0, 25.0, 12.5, 12.5, 2.5, 2.5, 0.25, 0.25])}
    }
    
    print("=========================================================================")
    print("РЕЗУЛЬТАТЫ РАСЧЕТА МНК С УЧЕТОМ ЭКСПЕРИМЕНТАЛЬНОЙ СЛУЧАЙНОЙ ПОГРЕШНОСТИ")
    print("=========================================================================")
    
    for anion, params in targets.items():
        c = params['x']
        k_target = params['k']
        n = len(c)
        
        # Generate area S = C / k_target + noise
        # We add a relative standard deviation of ~0.8%
        s_base = c / k_target
        noise = np.random.normal(0, 0.008 * s_base)
        s = s_base + noise
        
        # Ensure s is strictly positive
        s = np.clip(s, 1e-5, None)
        
        # 1. Model: C = k * S (through origin)
        # c = k * s -> k = sum(s*c)/sum(s^2)
        k_calc = np.sum(s * c) / np.sum(s**2)
        c_pred_orig = k_calc * s
        residuals_orig = c - c_pred_orig
        s_y_orig = np.sqrt(np.sum(residuals_orig**2) / (n - 1))
        s_k_calc = s_y_orig / np.sqrt(np.sum(s**2))
        t_student_orig = stats.t.ppf(0.975, n - 1)
        delta_k = t_student_orig * s_k_calc
        r_sq_orig = 1 - (np.sum(residuals_orig**2) / np.sum(c**2))
        
        # 2. Model: C = a * S + b (with intercept)
        mean_s = np.mean(s)
        mean_c = np.mean(c)
        var_s = np.sum((s - mean_s)**2)
        a = np.sum((s - mean_s) * (c - mean_c)) / var_s
        b = mean_c - a * mean_s
        c_pred = a * s + b
        residuals = c - c_pred
        s_y = np.sqrt(np.sum(residuals**2) / (n - 2))
        s_a = s_y / np.sqrt(var_s)
        s_b = s_y * np.sqrt(np.sum(s**2) / (n * var_s))
        t_student = stats.t.ppf(0.975, n - 2)
        delta_a = t_student * s_a
        delta_b = t_student * s_b
        r, _ = stats.pearsonr(s, c)
        r_sq = r**2
        
        print(f"\nАНИОН: {anion.upper()}")
        print(f"  Количество точек (n): {n}")
        print("  1) Модель через начало координат C = k * S:")
        print(f"     k (чувствительность): {k_calc:.6f}")
        print(f"     s_k:                  {s_k_calc:.6f}")
        print(f"     delta_k (P=0.95):     ±{delta_k:.6f}")
        print(f"     R^2:                  {r_sq_orig:.6f}")
        print(f"     s_y (мг/дм3):         {s_y_orig:.4f}")
        print(f"     Уравнение: C = ({k_calc:.4f} ± {delta_k:.4f}) * S".replace('.', ','))
        
        print("  2) Линейная модель со свободным членом C = a * S + b:")
        print(f"     a (угловой коэф.):    {a:.6f}")
        print(f"     s_a:                  {s_a:.6f}")
        print(f"     delta_a (P=0.95):     ±{delta_a:.6f}")
        print(f"     b (свободный член):   {b:.6f}")
        print(f"     s_b:                  {s_b:.6f}")
        print(f"     delta_b (P=0.95):     ±{delta_b:.6f}")
        print(f"     R^2:                  {r_sq:.6f}")
        print(f"     s_y (мг/дм3):         {s_y:.4f}")
        print(f"     Уравнение: C = ({a:.4f} ± {delta_a:.4f}) * S + ({b:.4f} ± {delta_b:.4f})".replace('.', ','))

if __name__ == '__main__':
    calculate_lsm_noisy()
