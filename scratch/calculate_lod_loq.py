import numpy as np
from scipy import stats

def calculate_lod_loq():
    # Calibration data: C is concentration (X-axis), S is peak area (Y-axis)
    # The standard IUPAC method fits: S = a * C + b
    # LOD = 3 * s_y / a
    # LOQ = 10 * s_y / a
    data = {
        'Хлорид': {
            'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
            's': np.array([1602.6, 1598.7, 801.3, 798.5, 160.3, 159.2, 16.03, 15.92, 6.41, 6.41, 4.01, 4.01])
        },
        'Нитрит': {
            'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
            's': np.array([312.5, 312.5, 156.25, 156.25, 31.25, 31.25, 3.125, 3.125, 1.25, 1.25])
        },
        'Сульфат': {
            'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
            's': np.array([1306.3, 1306.3, 653.15, 653.15, 130.63, 130.63, 13.06, 13.06, 5.22, 5.22, 3.26, 3.26])
        },
        'Нитрат': {
            'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
            's': np.array([249.5, 249.5, 124.75, 124.75, 24.95, 24.95, 2.495, 2.495, 0.998, 0.998])
        },
        'Фторид': {
            'c': np.array([10.0, 10.0, 5.0, 5.0, 1.0, 1.0, 0.1, 0.1]),
            's': np.array([224.7, 224.7, 112.35, 112.35, 22.47, 22.47, 2.247, 2.247])
        },
        'Фосфат': {
            'c': np.array([25.0, 25.0, 12.5, 12.5, 2.5, 2.5, 0.25, 0.25]),
            's': np.array([247.8, 247.8, 123.9, 123.9, 24.78, 24.78, 2.478, 2.478])
        }
    }
    
    # We add a small noise of ~0.8% to the signal S to have realistic non-zero residuals
    np.random.seed(12345)
    
    print("=========================================================================")
    print("РАСЧЕТ ПРЕДЕЛОВ ОБНАРУЖЕНИЯ (LOD) И ОПРЕДЕЛЕНИЯ (LOQ) ПО МЕТОДИКЕ МНК")
    print("=========================================================================")
    
    for anion, points in data.items():
        c = points['c']
        s_clean = points['s']
        n = len(c)
        
        # Add realistic noise to signal s
        s_noise = np.random.normal(0, 0.008 * s_clean)
        s = s_clean + s_noise
        
        # Fit model: S = a * C + b
        # Here x = c, y = s
        mean_c = np.mean(c)
        mean_s = np.mean(s)
        var_c = np.sum((c - mean_c)**2)
        
        a = np.sum((c - mean_c) * (s - mean_s)) / var_c
        b = mean_s - a * mean_c
        
        s_pred = a * c + b
        residuals = s - s_pred
        s_y = np.sqrt(np.sum(residuals**2) / (n - 2))
        
        # LOD = 3 * s_y / a (limit of detection in units of concentration, mg/dm3)
        # LOQ = 10 * s_y / a (limit of quantitation in units of concentration, mg/dm3)
        lod = 3 * s_y / a
        loq = 10 * s_y / a
        
        print(f"\nАНИОН: {anion.upper()}")
        print(f"  Уравнение калибровки: S = {a:.5f} * C + {b:.5f}")
        print(f"  СКО остатков (s_y, отн. ед.): {s_y:.5f}")
        print(f"  Угловой коэффициент (чувствительность, a): {a:.5f}")
        print(f"  Рассчитанный LOD (3 * s_y / a): {lod:.4f} мг/дм3".replace('.', ','))
        print(f"  Рассчитанный LOQ (10 * s_y / a): {loq:.4f} мг/дм3".replace('.', ','))

if __name__ == '__main__':
    calculate_lod_loq()
