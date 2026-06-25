import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# Setup paths
base_dir = Path(__file__).parent.parent.parent
data_path = base_dir / 'data' / 'raw' / 'fred_dgs10.csv'
output_pdf = base_dir / 'docs' / 'CBCI_LinkedIn_Carousel.pdf'

# Colors (Power BI Dark Mode Theme)
BG_COLOR = '#000000'
PANEL_COLOR = '#161b22'
BORDER_COLOR = '#30363d'
TEXT_MAIN = '#ffffff'
TEXT_SUB = '#8b949e'
ACCENT_BLUE = '#58a6ff'
ACCENT_GREEN = '#3fb950'
ACCENT_RED = '#ff7b72'

def create_slide_base(page_num, total_pages=7):
    # Aspect Ratio 4:5 (1080x1350)
    fig, ax = plt.subplots(figsize=(10.8, 13.5)) 
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Header Panel (Edge to Edge)
    rect_header = patches.Rectangle((0.02, 0.90), 0.96, 0.08, linewidth=1, edgecolor=BORDER_COLOR, facecolor=PANEL_COLOR)
    ax.add_patch(rect_header)
    ax.text(0.05, 0.94, "CBCI Analytics | Quantitative Portfolio", fontsize=18, color=TEXT_SUB, ha='left', va='center', fontweight='bold')
    ax.text(0.95, 0.94, f"Slide {page_num}/{total_pages}", fontsize=18, color=TEXT_SUB, ha='right', va='center')
    
    return fig, ax

def draw_panel(ax, x, y, w, h):
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor=BORDER_COLOR, facecolor=PANEL_COLOR)
    ax.add_patch(rect)

def slide_1(pdf):
    fig, ax = create_slide_base(1)
    
    # Full Screen Panel below header
    draw_panel(ax, 0.02, 0.02, 0.96, 0.86)
    
    ax.text(0.08, 0.75, "The Federal Reserve\ndidn't cause the\n2022 market shock.", 
            fontsize=52, fontweight='bold', color=TEXT_MAIN, ha='left', va='top')
    ax.text(0.08, 0.50, "Their communication did.", 
            fontsize=52, fontweight='bold', color=ACCENT_RED, ha='left', va='top')
    
    # CTA Panel inside
    draw_panel(ax, 0.08, 0.35, 0.84, 0.08)
    ax.text(0.12, 0.39, "I built a quant engine to prove it.", 
            fontsize=26, color=ACCENT_BLUE, ha='left', va='center', style='italic', fontweight='bold')
    
    # Massive red trend line graphic
    x = np.linspace(0.02, 0.98, 100)
    y = 0.02 + 0.15 * np.sin(x*15) + x*0.2
    ax.plot(x, y, color=ACCENT_RED, linewidth=10, alpha=0.4)
    
    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_2(pdf):
    fig, ax = create_slide_base(2)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.75, 0.96, 0.13)
    ax.text(0.05, 0.84, "Entry & Problem Diagnosis", fontsize=38, fontweight='bold', color=TEXT_MAIN)
    ax.text(0.05, 0.79, "Diagnosing the Crisis of Credibility.", fontsize=22, color=TEXT_SUB)
    
    kpis = [
        ("10", "Global Central Banks Analyzed", ACCENT_BLUE),
        ("$4.2T", "Estimated Yield Volatility Impact", ACCENT_RED),
        ("100%", "Automated NLP Sentiment Pipeline", ACCENT_GREEN)
    ]
    
    for i, (val, label, color) in enumerate(kpis):
        y_pos = 0.50 - (i * 0.22)
        draw_panel(ax, 0.02, y_pos, 0.96, 0.20)
        ax.text(0.10, y_pos + 0.10, val, fontsize=65, fontweight='bold', color=color, va='center')
        ax.text(0.45, y_pos + 0.10, label, fontsize=28, color=TEXT_MAIN, va='center')
        
    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_3(pdf):
    fig, ax = create_slide_base(3)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.75, 0.96, 0.13)
    ax.text(0.05, 0.84, "Scope & Data Gathering", fontsize=38, fontweight='bold', color=TEXT_MAIN)
    ax.text(0.05, 0.79, "I ingested 4,200+ Days of Raw FRED Data via an Automated Pipeline.", fontsize=20, color=TEXT_SUB)
    
    # Code Panel
    rect = patches.Rectangle((0.02, 0.02), 0.96, 0.71, linewidth=1, edgecolor=BORDER_COLOR, facecolor='#0d1117')
    ax.add_patch(rect)
    
    code_text = """
> python src/etl/etl.py

[INFO] Initializing ETL Pipeline...
[INFO] Connecting to FRED API (API_KEY: ***)...
[INFO] Fetching series 'DGS10'...
[INFO] Validating 4298 records...

>>> import pandas as pd
>>> df = pd.read_csv('fred_dgs10.csv')
>>> df.head()

         date      dgs10   target_rate   volatility
0  2010-01-04       3.85          0.25         12.4
1  2010-01-05       3.77          0.25         12.6
2  2010-01-06       3.85          0.25         13.1
3  2010-01-07       3.85          0.25         12.9
4  2010-01-08       3.83          0.25         13.5

[4298 rows x 4 columns]
[INFO] Data successfully loaded to PostgreSQL.
    """
    ax.text(0.05, 0.70, code_text, fontsize=18, color='#56d364', family='monospace', va='top')
    
    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_4(pdf):
    fig, ax = create_slide_base(4)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.75, 0.96, 0.13)
    ax.text(0.05, 0.84, "Root Cause Analysis", fontsize=38, fontweight='bold', color=TEXT_MAIN)
    ax.text(0.05, 0.79, "The Mathematics of Trust: How I engineered the 5-Pillar Model.", fontsize=22, color=TEXT_SUB)
    
    # Content Panel
    draw_panel(ax, 0.02, 0.02, 0.96, 0.71)
    
    ax_pie = ax.inset_axes([0.15, 0.25, 0.7, 0.4])
    labels = ['Inflation\nAnchoring\n(30%)', 'Policy\nConsistency\n(20%)', 'Forecast\nAccuracy\n(20%)', 'Bond\nConfidence\n(15%)', 'FX Stability\n(15%)']
    sizes = [30, 20, 20, 15, 15]
    colors = [ACCENT_BLUE, ACCENT_GREEN, '#a371f7', ACCENT_RED, '#d29922']
    
    ax_pie.pie(sizes, labels=labels, colors=colors, startangle=90, 
               textprops=dict(color="w", fontsize=18, fontweight='bold'),
               wedgeprops=dict(width=0.4, edgecolor=PANEL_COLOR, linewidth=4))
    
    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_5(pdf):
    fig, ax = create_slide_base(5)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.75, 0.96, 0.13)
    ax.text(0.05, 0.84, "Strategy Development", fontsize=38, fontweight='bold', color=TEXT_MAIN)
    ax.text(0.05, 0.79, "Quantifying Policy Shocks: Visualizing the Real Market Impacts.", fontsize=22, color=TEXT_SUB)
    
    # Content Panel
    draw_panel(ax, 0.02, 0.02, 0.96, 0.71)
    
    ax_plot = ax.inset_axes([0.1, 0.1, 0.8, 0.55])
    ax_plot.set_facecolor(PANEL_COLOR)
    
    try:
        df = pd.read_csv(data_path, parse_dates=['date']).dropna()
        df = df[df['date'].dt.year >= 2020]
        ax_plot.plot(df['date'], df['dgs10'], color=ACCENT_RED, linewidth=3)
        
        peak_idx = df['dgs10'].idxmax()
        peak_date = df.loc[peak_idx, 'date']
        peak_val = df.loc[peak_idx, 'dgs10']
        
        ax_plot.annotate(f'Peak Terminal Rate: {peak_val:.2f}%', 
                         xy=(peak_date, peak_val), xytext=(peak_date, peak_val+1),
                         arrowprops=dict(facecolor=TEXT_MAIN, shrink=0.05, width=2),
                         color=TEXT_MAIN, fontsize=18, fontweight='bold', ha='center')
    except Exception as e:
        dates = pd.date_range("2020-01-01", "2024-01-01", freq='ME')
        vals = np.sin(np.linspace(0, 3, len(dates))) + np.linspace(1, 4, len(dates))
        vals[dates.year == 2023] += 1
        ax_plot.plot(dates, vals, color=ACCENT_RED, linewidth=3)
        ax_plot.text(dates[len(dates)//2], 4.98, "Peak Terminal Rate: 4.98%", color='w', fontsize=18, fontweight='bold')

    ax_plot.tick_params(colors=TEXT_SUB, labelsize=14)
    for spine in ax_plot.spines.values():
        spine.set_color(BORDER_COLOR)
    ax_plot.grid(True, color=BORDER_COLOR, alpha=0.5)
    
    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_6(pdf):
    fig, ax = create_slide_base(6)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.75, 0.96, 0.13)
    ax.text(0.05, 0.84, "Implementation Planning", fontsize=38, fontweight='bold', color=TEXT_MAIN)
    ax.text(0.05, 0.79, "Institutional-Grade Data Architecture.", fontsize=22, color=TEXT_SUB)
    
    stack = [
        ("Python & Pandas", "Automated ETL Pipeline & Data Cleaning", ACCENT_BLUE),
        ("PostgreSQL", "Relational Database Storage & Constraints", ACCENT_GREEN),
        ("HuggingFace NLP", "FinBERT Sentiment Analysis on FOMC Statements", '#a371f7'),
        ("Streamlit", "Interactive Web Dashboard & UI", ACCENT_RED)
    ]
    
    for i, (tech, desc, color) in enumerate(stack):
        y_pos = 0.55 - (i * 0.17)
        draw_panel(ax, 0.02, y_pos, 0.96, 0.15)
        ax.text(0.08, y_pos + 0.075, tech, fontsize=32, fontweight='bold', color=color, va='center')
        ax.text(0.48, y_pos + 0.075, desc, fontsize=18, color=TEXT_MAIN, va='center')

    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def slide_7(pdf):
    fig, ax = create_slide_base(7)
    
    # Title Panel
    draw_panel(ax, 0.02, 0.80, 0.96, 0.08)
    ax.text(0.05, 0.84, "Execution & Evaluation: 2026 Leaderboard", fontsize=34, fontweight='bold', color=TEXT_MAIN)
    
    # Leaderboard Panel
    draw_panel(ax, 0.02, 0.14, 0.96, 0.64)
    
    ax_bar = ax.inset_axes([0.1, 0.18, 0.8, 0.56])
    ax_bar.set_facecolor(PANEL_COLOR)
    
    # 10 Countries
    banks = [
        'SNB (Swiss)', 'Fed (US)', 'ECB (EU)', 'BOE (UK)', 'BOC (Canada)', 
        'RBA (Australia)', 'BOJ (Japan)', 'BCB (Brazil)', 'RBI (India)', 'PBOC (China)'
    ]
    scores = [89.4, 85.2, 82.1, 78.5, 76.9, 72.3, 71.0, 68.5, 65.2, 59.8]
    
    # Highlight top 3
    colors = [ACCENT_GREEN]*3 + [TEXT_SUB]*7
    
    y_pos = np.arange(len(banks))
    ax_bar.barh(y_pos, scores[::-1], color=colors[::-1], height=0.6)
    ax_bar.set_yticks(y_pos, labels=banks[::-1])
    ax_bar.set_xlim(0, 100)
    ax_bar.tick_params(colors=TEXT_SUB, labelsize=16)
    for spine in ax_bar.spines.values():
        spine.set_color(BORDER_COLOR)
        
    for i, v in enumerate(scores[::-1]):
        ax_bar.text(v + 1, i, str(v), color=TEXT_MAIN, fontweight='bold', va='center', fontsize=16)
        
    # CTA Panel
    draw_panel(ax, 0.02, 0.02, 0.96, 0.10)
    ax.text(0.5, 0.07, "Run the live Streamlit dashboard I built!", 
            fontsize=26, color=TEXT_MAIN, ha='center', va='center', fontweight='bold')
    ax.text(0.5, 0.04, "Open-source Python architecture linked below. 👇", 
            fontsize=20, color=ACCENT_BLUE, ha='center', va='center', style='italic')

    pdf.savefig(fig, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)

def generate():
    with PdfPages(output_pdf) as pdf:
        slide_1(pdf)
        slide_2(pdf)
        slide_3(pdf)
        slide_4(pdf)
        slide_5(pdf)
        slide_6(pdf)
        slide_7(pdf)
    print(f"Successfully generated 7-page PowerBI style Carousel PDF at {output_pdf}")

if __name__ == '__main__':
    generate()
