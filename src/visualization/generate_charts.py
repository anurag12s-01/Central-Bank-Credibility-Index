import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
from pathlib import Path
import matplotlib.dates as mdates

# Set up paths
base_dir = Path(__file__).parent.parent.parent
data_file = base_dir / 'data' / 'raw' / 'fred_dgs10.csv'
output_dir = base_dir / 'docs' / 'images'

# Configure ultra-premium GitHub Dark Mode style
plt.style.use('dark_background')
sns.set_theme(style='darkgrid', rc={
    'axes.facecolor': '#0d1117', 
    'figure.facecolor': '#0d1117', 
    'grid.color': '#30363d', 
    'text.color': '#c9d1d9', 
    'axes.labelcolor': '#c9d1d9', 
    'xtick.color': '#c9d1d9', 
    'ytick.color': '#c9d1d9'
})

def generate_policy_shock_chart():
    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['value', 'date'])
    df = df.sort_values('date')
    
    # Calculate Technical Moving Averages
    df['SMA_50'] = df['value'].rolling(window=50).mean()
    df['SMA_200'] = df['value'].rolling(window=200).mean()
    
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    
    # Plot Yield and MAs
    ax.plot(df['date'], df['value'], color='#58a6ff', linewidth=1.5, label='10-Year Treasury Yield (DGS10)')
    ax.plot(df['date'], df['SMA_50'], color='#ff7b72', linewidth=1.2, linestyle='--', label='50-Day Moving Average')
    ax.fill_between(df['date'], df['value'], color='#58a6ff', alpha=0.1)
    
    # Highlight major macroeconomic crises / shocks
    covid_start = pd.to_datetime('2020-02-01')
    covid_end = pd.to_datetime('2021-03-01')
    ax.axvspan(covid_start, covid_end, color='#ff7b72', alpha=0.15, label='Pandemic Shock / ZIRP')
    
    inflation_start = pd.to_datetime('2022-03-01')
    inflation_end = pd.to_datetime('2023-12-01')
    ax.axvspan(inflation_start, inflation_end, color='#d2a8ff', alpha=0.15, label='Aggressive Hiking Cycle')
    
    # Annotations
    max_idx = df['value'].idxmax()
    max_date = df.loc[max_idx, 'date']
    max_val = df.loc[max_idx, 'value']
    
    # Add headroom to the top of the chart so the label isn't squished
    ax.set_ylim(top=max_val + 1.2)
    
    ax.scatter(max_date, max_val, color='#ff7b72', s=120, zorder=5)
    ax.annotate(f'Terminal Rate Peak: {max_val}%\n{max_date.strftime("%b %Y")}', 
                (max_date, max_val), textcoords='offset points', xytext=(-90, -15), 
                ha='center', color='#ff7b72', fontweight='bold', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.4', fc='#0d1117', ec='#ff7b72', alpha=0.9))
    
    # Styling
    ax.set_title('Macro Policy Shock Monitor: 10-Year Treasury Yield Dynamics', fontsize=20, pad=20, fontweight='bold', color='#ffffff')
    ax.set_xlabel('Timeline (2010 - 2026)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Yield (%)', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', frameon=True, facecolor='#21262d', edgecolor='#30363d', fontsize=11)
    
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    
    plt.tight_layout()
    plt.savefig(output_dir / 'policy_shock_preview.png', bbox_inches='tight')
    plt.close()

def generate_rankings_chart():
    # Authentic data pulled from the ETL pipeline
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'processed', 'authentic_cbci_scores.csv'))
    df = df.sort_values('Total Score', ascending=True)
    
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    
    # Premium Colors for the 5 pillars
    colors = ['#3fb950', '#58a6ff', '#a371f7', '#d2a8ff', '#ff7b72']
    pillars = df.columns[1:6]
    
    # Plot horizontal stacked bar chart
    lefts = np.zeros(len(df))
    for idx, pillar in enumerate(pillars):
        ax.barh(df['Central Bank'], df[pillar], left=lefts, color=colors[idx], label=pillar, height=0.6, edgecolor='#0d1117', linewidth=1.5)
        lefts += df[pillar]
        
    ax.set_title('Global Central Bank Credibility Index (CBCI) - Methodological Breakdown', fontsize=20, pad=20, fontweight='bold', color='#ffffff')
    ax.set_xlabel('Composite Credibility Score (0-100)', fontsize=14, fontweight='bold')
    
    # Add Total Score labels at the end of each bar
    for i, total in enumerate(df['Total Score']):
        ax.text(total + 1.5, i, f'{total:.1f}', va='center', ha='left', color='#ffffff', fontweight='bold', fontsize=12)
                 
    ax.set_xlim(0, 105)
    ax.grid(axis='x', color='#30363d', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#30363d')
    ax.spines['bottom'].set_color('#30363d')
    
    # Place legend nicely at the bottom
    ax.legend(loc='upper left', bbox_to_anchor=(0, -0.1), ncol=5, frameon=False, fontsize=11, labelcolor='#c9d1d9')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'global_rankings_preview.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    generate_policy_shock_chart()
    generate_rankings_chart()
    print('Highly detailed authentic charts generated successfully!')
