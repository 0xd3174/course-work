import numpy as np
from scipy import stats

def calculate_lsm_for_anions():
    # Calibration data: X is concentration (mg/dm3), Y is peak area (relative units)
    # We define duplicates based on the experimental standard solution concentrations and OCR readings
    data = {
        'Хлорид': {
            'x': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
            'y': np.array([24.56, 25.35, 12.55, 12.71, 2.46, 2.54, 0.246, 0.254, 0.104, 0.090, 0.069, 0.062])
        },
        'Нитрит': {
            'x': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
            'y': np.array([8.02, 7.98, 4.01, 3.99, 0.805, 0.795, 0.081, 0.079, 0.033, 0.031])
        },
        'Сульфат': {
            'x': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
            'y': np.array([30.82, 30.62, 15.42, 15.20, 3.08, 3.04, 0.308, 0.304, 0.123, 0.121, 0.078, 0.076])
        },
        'Нитрат': {
            'x': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
            'y': np.array([10.025, 9.890, 4.940, 5.000, 1.070, 1.055, 0.100, 0.089, 0.040, 0.040])
        },
        'Фторид': {
            'x': np.array([10.0, 10.0, 5.0, 5.0, 1.0, 1.0, 0.1, 0.1]),
            'y': np.array([0.448, 0.442, 0.224, 0.221, 0.045, 0.044, 0.0046, 0.0044])
        },
        'Фосфат': {
            'x': np.array([25.0, 25.0, 12.5, 12.5, 2.5, 2.5, 0.25, 0.25]),
            'y': np.array([2.540, 2.500, 1.270, 1.250, 0.254, 0.250, 0.026, 0.024])
        }
    }
    
    print("==================================================================================")
    print("РЕЗУЛЬТАТЫ РАСЧЕТА МЕТОДОМ НАИМЕНЬШИХ КВАДРАТОВ (МНК) ДЛЯ ГРАДУИРОВОК АНИОНОВ")
    print("==================================================================================")
    
    for anion, points in data.items():
        x = points['x']
        y = points['y']
        n = len(x)
        
        # 1. Model with intercept: y = a * x + b
        # Using standard formulas
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        var_x = np.sum((x - mean_x)**2)
        
        a = np.sum((x - mean_x) * (y - mean_y)) / var_x
        b = mean_y - a * mean_x
        
        y_pred = a * x + b
        residuals = y - y_pred
        s_y = np.sqrt(np.sum(residuals**2) / (n - 2))
        
        s_a = s_y / np.sqrt(var_x)
        s_b = s_y * np.sqrt(np.sum(x**2) / (n * var_x))
        
        # Student t-factor for P=0.95, f=n-2
        t_student_2 = stats.t.ppf(0.975, n - 2)
        delta_a = t_student_2 * s_a
        delta_b = t_student_2 * s_b
        
        r, _ = stats.pearsonr(x, y)
        r_sq = r**2
        
        # 2. Model through origin: y = a_orig * x
        a_orig = np.sum(x * y) / np.sum(x**2)
        y_pred_orig = a_orig * x
        residuals_orig = y - y_pred_orig
        s_y_orig = np.sqrt(np.sum(residuals_orig**2) / (n - 1))
        s_a_orig = s_y_orig / np.sqrt(np.sum(x**2))
        
        # Student t-factor for P=0.95, f=n-1
        t_student_1 = stats.t.ppf(0.975, n - 1)
        delta_a_orig = t_student_1 * s_a_orig
        
        # Calculate R^2 for model through origin: R^2 = 1 - sum(e_i^2)/sum((y_i)^2)
        r_sq_orig = 1 - (np.sum(residuals_orig**2) / np.sum(y**2))
        
        print(f"\nАНИОН: {anion.upper()}")
        print(f"Количество точек (n): {n}")
        print("  Модель без свободного члена (прохождение через начало координат: y = k * C):")
        print(f"    Коэффициент k (чувствительность): {a_orig:.5f}")
        print(f"    Стандартная ошибка s_k: {s_a_orig:.5f}")
        print(f"    Доверительный интервал delta_k (P=0.95, f={n-1}, t={t_student_1:.3f}): ± {delta_a_orig:.5f}")
        print(f"    Итоговое уравнение: y = ({a_orig:.4f} ± {delta_a_orig:.4f}) * C".replace('.', ','))
        print(f"    Коэффициент детерминации R^2: {r_sq_orig:.5f}".replace('.', ','))
        print(f"    Стандартное отклонение остатков s_y: {s_y_orig:.5f}".replace('.', ','))
        
        print("  Модель со свободным членом (y = a * C + b):")
        print(f"    Угловой коэффициент a: {a:.5f}")
        print(f"    Доверительный интервал delta_a: ± {delta_a:.5f}")
        print(f"    Свободный член b: {b:.5f}")
        print(f"    Доверительный интервал delta_b: ± {delta_b:.5f}")
        print(f"    Итоговое уравнение: y = ({a:.4f} ± {delta_a:.4f}) * C + ({b:.4f} ± {delta_b:.4f})".replace('.', ','))
        print(f"    Коэффициент детерминации R^2: {r_sq:.5f}".replace('.', ','))
        print(f"    Стандартное отклонение остатков s_y: {s_y:.5f}".replace('.', ','))

if __name__ == '__main__':
    calculate_lsm_for_anions()
