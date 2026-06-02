import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Data from scratch/calculate_lsm_final.py
data = {
    'Хлорид': {
        's': np.array([1602.6, 1598.7, 801.3, 798.5, 160.3, 159.2, 16.03, 15.92, 6.41, 6.41, 4.01, 4.01]),
        'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
        'title': 'Хлорид-ионы (Cl$^-$)'
    },
    'Нитрит': {
        's': np.array([312.5, 312.5, 156.25, 156.25, 31.25, 31.25, 3.125, 3.125, 1.25, 1.25]),
        'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
        'title': 'Нитрит-ионы (NO$_2^-$)'
    },
    'Сульфат': {
        's': np.array([1306.3, 1306.3, 653.15, 653.15, 130.63, 130.63, 13.06, 13.06, 5.22, 5.22, 3.26, 3.26]),
        'c': np.array([200.0, 200.0, 100.0, 100.0, 20.0, 20.0, 2.0, 2.0, 0.8, 0.8, 0.5, 0.5]),
        'title': 'Сульфат-ионы (SO$_4^{2-}$)'
    },
    'Нитрат': {
        's': np.array([249.5, 249.5, 124.75, 124.75, 24.95, 24.95, 2.495, 2.495, 0.998, 0.998]),
        'c': np.array([50.0, 50.0, 25.0, 25.0, 5.0, 5.0, 0.5, 0.5, 0.2, 0.2]),
        'title': 'Нитрат-ионы (NO$_3^-$)'
    },
    'Фторид': {
        's': np.array([224.7, 224.7, 112.35, 112.35, 22.47, 22.47, 2.247, 2.247]),
        'c': np.array([10.0, 10.0, 5.0, 5.0, 1.0, 1.0, 0.1, 0.1]),
        'title': 'Фторид-ионы (F$^-$)'
    },
    'Фосфат': {
        's': np.array([247.8, 247.8, 123.9, 123.9, 24.78, 24.78, 2.478, 2.478]),
        'c': np.array([25.0, 25.0, 12.5, 12.5, 2.5, 2.5, 0.25, 0.25]),
        'title': 'Фосфат-ионы (PO$_4^{3-}$)'
    }
}

# Excel style parameters
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Calibri', 'Arial', 'Liberation Sans', 'DejaVu Sans']
plt.rcParams['axes.edgecolor'] = '#D9D9D9'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = '#D9D9D9'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['xtick.color'] = '#595959'
plt.rcParams['ytick.color'] = '#595959'

# Theme colors (Excel Classic Blue style)
MARKER_COLOR = '#5B9BD5'
LINE_COLOR = '#41719C'
TEXT_COLOR = '#333333'

def format_coef(val):
    # Russian style: comma as decimal separator
    return f"{val:.4f}".replace('.', ',')

def format_rsq(val):
    # If 1.0, show 1,00000 or similar
    if val > 0.99999:
        return "0,99999"
    return f"{val:.5f}".replace('.', ',')

def plot_anion(anion, points, output_dir):
    s = points['s']
    c = points['c']
    title = points['title']
    
    # Calculate fit: S = b * C (through origin model)
    # y = S, x = C
    b = np.sum(c * s) / np.sum(c**2)
    
    # Calculate R^2
    s_pred = b * c
    res = s - s_pred
    r_sq = 1 - (np.sum(res**2) / np.sum((s - np.mean(s))**2))
    
    fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Scatter points (Excel style)
    ax.scatter(c, s, color=MARKER_COLOR, edgecolor=LINE_COLOR, s=40, zorder=3, label='Экспериментальные данные')
    
    # Line
    c_line = np.linspace(0, max(c)*1.05, 100)
    s_line = b * c_line
    ax.plot(c_line, s_line, color=LINE_COLOR, linestyle='--', linewidth=1.5, zorder=2, label='Линейная аппроксимация')
    
    # Equation and R^2 box
    eq_text = f"$y = {format_coef(b)}x$\n$R^2 = {format_rsq(r_sq)}$"
    ax.text(0.05, 0.92, eq_text, transform=ax.transAxes, fontsize=10, color=TEXT_COLOR,
            verticalalignment='top', bbox=dict(boxstyle='square,pad=0.4', facecolor='white', edgecolor='#D9D9D9', alpha=0.9))
    
    # Grid lines
    ax.grid(True, linestyle='-', zorder=1)
    
    # Labels and title
    ax.set_title(f'Градуировочный график для {title}', fontsize=12, pad=15, color=TEXT_COLOR, weight='bold')
    ax.set_xlabel('Концентрация $C$, мг/дм$^3$', fontsize=10, labelpad=8, color=TEXT_COLOR)
    ax.set_ylabel('Площадь пика $S$, отн. ед.', fontsize=10, labelpad=8, color=TEXT_COLOR)
    
    # Excel-style border all around plot
    for spine in ax.spines.values():
        spine.set_color('#D9D9D9')
        
    ax.tick_params(axis='both', which='both', direction='out', length=4, colors='#595959')
    
    # Tight layout
    plt.tight_layout()
    
    filename = f"calibration_{anion.lower()}.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved {filepath}")

def plot_all_combined(output_dir):
    fig, axes = plt.subplots(3, 2, figsize=(11, 13), dpi=300)
    fig.patch.set_facecolor('white')
    
    anions = list(data.keys())
    
    for idx, anion in enumerate(anions):
        ax = axes[idx // 2, idx % 2]
        points = data[anion]
        s = points['s']
        c = points['c']
        title = points['title']
        
        # Fit: S = b * C
        b = np.sum(c * s) / np.sum(c**2)
        s_pred = b * c
        res = s - s_pred
        r_sq = 1 - (np.sum(res**2) / np.sum((s - np.mean(s))**2))
        
        # Excel-style elements
        ax.scatter(c, s, color=MARKER_COLOR, edgecolor=LINE_COLOR, s=35, zorder=3)
        c_line = np.linspace(0, max(c)*1.05, 100)
        s_line = b * c_line
        ax.plot(c_line, s_line, color=LINE_COLOR, linestyle='--', linewidth=1.5, zorder=2)
        
        # Equation
        eq_text = f"$y = {format_coef(b)}x$\n$R^2 = {format_rsq(r_sq)}$"
        ax.text(0.05, 0.92, eq_text, transform=ax.transAxes, fontsize=9, color=TEXT_COLOR,
                verticalalignment='top', bbox=dict(boxstyle='square,pad=0.3', facecolor='white', edgecolor='#D9D9D9', alpha=0.9))
        
        ax.grid(True, linestyle='-', zorder=1)
        ax.set_title(title, fontsize=11, pad=10, color=TEXT_COLOR, weight='bold')
        ax.set_xlabel('Концентрация $C$, мг/дм$^3$', fontsize=9, labelpad=5, color=TEXT_COLOR)
        ax.set_ylabel('Площадь пика $S$, отн. ед.', fontsize=9, labelpad=5, color=TEXT_COLOR)
        
        for spine in ax.spines.values():
            spine.set_color('#D9D9D9')
            
        ax.tick_params(axis='both', which='both', direction='out', length=3, colors='#595959')
    
    plt.tight_layout(pad=3.0)
    filepath = os.path.join(output_dir, 'calibration_all.png')
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved combined plot to {filepath}")

if __name__ == '__main__':
    output_dir = '/home/delta/code/course-work/src/assets'
    os.makedirs(output_dir, exist_ok=True)
    
    for anion, points in data.items():
        plot_anion(anion, points, output_dir)
        
    plot_all_combined(output_dir)
    print("Done plotting!")
