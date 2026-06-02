import numpy as np
from scipy import stats

def calculate_lsm_c_vs_s_detailed():
    data = {
        'Хлорид': {
            's': np.array([1602.6, 1598.7, 801.3, 798.5, 160.3, 159.2, 16.03, 15.92, 6.41, 6.41, 4.01, 4.01]),
            'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5])
        },
        'Нитрит': {
            's': np.array([312.5, 312.5, 156.25, 156.25, 31.25, 31.25, 3.125, 3.125, 1.25, 1.25]),
            'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2])
        },
        'Сульфат': {
            's': np.array([1306.3, 1306.3, 653.15, 653.15, 130.63, 130.63, 13.06, 13.06, 5.22, 5.22, 3.26, 3.26]),
            'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5])
        },
        'Нитрат': {
            's': np.array([249.5, 249.5, 124.75, 124.75, 24.95, 24.95, 2.495, 2.495, 0.998, 0.998]),
            'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2])
        },
        'Фторид': {
            's': np.array([224.7, 224.7, 112.35, 112.35, 22.47, 22.47, 2.247, 2.247]),
            'c': np.array([10.0, 10.0, 5.0, 5.0, 1.0, 1.0, 0.1, 0.1])
        },
        'Фосфат': {
            's': np.array([247.8, 247.8, 123.9, 123.9, 24.78, 24.78, 2.478, 2.478]),
            'c': np.array([25.0, 25.0, 12.5, 12.5, 2.5, 2.5, 0.25, 0.25])
        }
    }
    
    print("=========================================================================")
    print("ДЕТАЛЬНЫЙ РАСЧЕТ МНК ДЛЯ ДВУХ МОДЕЛЕЙ ГРАДУИРОВКИ (C = a * S и C = a * S + b)")
    print("=========================================================================")
    
    for anion, points in data.items():
        s = points['s']
        c = points['c']
        n = len(s)
        
        # 1. Model: C = a * S (through origin)
        a_orig = np.sum(s * c) / np.sum(s**2)
        c_pred_orig = a_orig * s
        res_orig = c - c_pred_orig
        s_y_orig = np.sqrt(np.sum(res_orig**2) / (n - 1))
        s_a_orig = s_y_orig / np.sqrt(np.sum(s**2))
        t_student_orig = stats.t.ppf(0.975, n - 1)
        delta_a_orig = t_student_orig * s_a_orig
        r_sq_orig = 1 - (np.sum(res_orig**2) / np.sum(c**2))
        
        # 2. Model: C = a * S + b (with intercept)
        mean_s = np.mean(s)
        mean_c = np.mean(c)
        var_s = np.sum((s - mean_s)**2)
        a = np.sum((s - mean_s) * (c - mean_c)) / var_s
        b = mean_c - a * mean_s
        c_pred = a * s + b
        res = c - c_pred
        s_y = np.sqrt(np.sum(res**2) / (n - 2))
        s_a = s_y / np.sqrt(var_s)
        s_b = s_y * np.sqrt(np.sum(s**2) / (n * var_s))
        t_student = stats.t.ppf(0.975, n - 2)
        delta_a = t_student * s_a
        delta_b = t_student * s_b
        r, _ = stats.pearsonr(s, c)
        r_sq = r**2
        
        print(f"\nАНАЛИТ: {anion.upper()}")
        print(f"  Количество точек (n): {n}")
        print("  1) Модель через начало координат C = k * S:")
        print(f"     k (чувствительность): {a_orig:.6f}")
        print(f"     s_k:                  {s_a_orig:.6f}")
        print(f"     delta_k (P=0.95):     ±{delta_a_orig:.6f}")
        print(f"     R^2:                  {r_sq_orig:.6f}")
        print(f"     s_y:                  {s_y_orig:.6f}")
        print(f"     Уравнение: C = ({a_orig:.4f} ± {delta_a_orig:.4f}) * S".replace('.', ','))
        
        print("  2) Линейная модель со свободным членом C = a * S + b:")
        print(f"     a (угловой коэф.):    {a:.6f}")
        print(f"     s_a:                  {s_a:.6f}")
        print(f"     delta_a (P=0.95):     ±{delta_a:.6f}")
        print(f"     b (свободный член):   {b:.6f}")
        print(f"     s_b:                  {s_b:.6f}")
        print(f"     delta_b (P=0.95):     ±{delta_b:.6f}")
        print(f"     R^2:                  {r_sq:.6f}")
        print(f"     s_y:                  {s_y:.6f}")
        print(f"     Уравнение: C = ({a:.4f} ± {delta_a:.4f}) * S + ({b:.4f} ± {delta_b:.4f})".replace('.', ','))

if __name__ == '__main__':
    calculate_lsm_c_vs_s_detailed()
