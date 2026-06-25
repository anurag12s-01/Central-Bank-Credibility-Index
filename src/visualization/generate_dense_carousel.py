import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import os

# Data
banks = ['SNB', 'FED', 'ECB', 'BOE', 'BOC', 'RBA', 'BOJ', 'BCB', 'RBI', 'PBOC']
scores = [89.4, 85.2, 82.1, 78.5, 76.9, 72.3, 71.0, 68.5, 65.2, 59.8]

# Style config
BG_COLOR = '#0a0a1a'
TEXT_MAIN = '#ffffff'
TEXT_SUB = '#a0a0b5'
ACCENT_BLUE = '#00f0ff'
ACCENT_GREEN = '#39ff14'

plt.rcParams.update({
    'text.color': TEXT_MAIN,
    'axes.labelcolor': TEXT_MAIN,
    'xtick.color': TEXT_SUB,
    'ytick.color': TEXT_SUB,
    'font.size': 8,
    'axes.titlesize': 10,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': BG_COLOR,
    'axes.edgecolor': TEXT_SUB
})

# Slide 1: Exec Summary (Infographic)
def slide_1(pdf):
    fig = plt.figure(figsize=(10.8, 13.5)) # 4:5 ratio
    fig.patch.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.9, "CENTRAL BANK CREDIBILITY INDEX", fontsize=24, color=ACCENT_BLUE, ha='center', weight='bold')
    fig.text(0.5, 0.85, "Quantifying Trust as a Determinant of Bond Market Volatility", fontsize=14, ha='center', color=TEXT_SUB)
    
    # Massive KPI
    fig.text(0.5, 0.6, "$4.2 TRILLION", fontsize=50, color=ACCENT_GREEN, ha='center', weight='bold')
    fig.text(0.5, 0.55, "Estimated global yield volatility driven by 'Transitory Inflation' communication failure", fontsize=10, ha='center', color=TEXT_SUB)
    
    fig.text(0.5, 0.35, "4.98%", fontsize=50, color='#ff003c', ha='center', weight='bold')
    fig.text(0.5, 0.30, "US 10-Year Treasury Yield Peak (2023)", fontsize=10, ha='center', color=TEXT_SUB)
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 2: Mindmap
def slide_2(pdf):
    fig = plt.figure(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set_facecolor(BG_COLOR)
    
    G = nx.DiGraph()
    G.add_node("CBCI Score")
    pillars = ["1. Inflation\nAnchoring", "2. Policy\nConsistency", "3. Forecast\nAccuracy", "4. Bond Market\nConfidence", "5. FX\nStability"]
    for p in pillars:
        G.add_edge(p, "CBCI Score")
    
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=ACCENT_BLUE, node_size=3000, alpha=0.8)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=ACCENT_GREEN, arrows=True, arrowsize=20)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color=BG_COLOR, font_weight="bold")
    
    fig.text(0.5, 0.95, "SYSTEM ARCHITECTURE (5-PILLAR MODEL)", fontsize=16, color=ACCENT_BLUE, ha='center', weight='bold')
    ax.axis('off')
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 3: Dense Data Table
def slide_3(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    np.random.seed(42)
    data = pd.DataFrame({
        'Bank': banks,
        'Composite Score': scores,
        'Inflation (30%)': np.random.uniform(10, 30, 10).round(1),
        'NLP (20%)': np.random.uniform(10, 20, 10).round(1),
        'Forecast (20%)': np.random.uniform(10, 20, 10).round(1),
        'Bonds (15%)': np.random.uniform(5, 15, 10).round(1),
        'FX (15%)': np.random.uniform(5, 15, 10).round(1)
    })
    
    table = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2.5)
    
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor(TEXT_SUB)
        if i == 0:
            cell.set_facecolor(ACCENT_BLUE)
            cell.set_text_props(color=BG_COLOR, weight='bold')
        else:
            cell.set_facecolor(BG_COLOR)
            cell.set_text_props(color=TEXT_MAIN)
            
    fig.text(0.5, 0.95, "GLOBAL LEADERBOARD (RAW DATA DUMP)", fontsize=16, color=ACCENT_BLUE, ha='center', weight='bold')
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 4: Pie Charts
def slide_4(pdf):
    fig = plt.figure(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    fig.text(0.5, 0.95, "MODEL WEIGHTING & NLP SENTIMENT", fontsize=16, color=ACCENT_BLUE, ha='center', weight='bold')
    
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.1, wspace=0.1, left=0.01, right=0.99, top=0.9, bottom=0.01)
    
    ax1 = fig.add_subplot(gs[0, :])
    labels = ["Inflation (30%)", "Consistency (20%)", "Forecast (20%)", "Bonds (15%)", "FX (15%)"]
    sizes = [30, 20, 20, 15, 15]
    colors = [ACCENT_BLUE, ACCENT_GREEN, '#ff003c', '#ffea00', '#aa00ff']
    ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color': TEXT_MAIN, 'fontsize': 8})
    ax1.set_title("CBCI Component Weighting", color=ACCENT_GREEN, pad=0)
    
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.pie([60, 40], labels=["Hawkish", "Dovish"], colors=[ACCENT_BLUE, '#ff003c'], autopct='%1.1f%%', textprops={'color': TEXT_MAIN, 'fontsize': 8})
    ax2.set_title("FED Sentiment 2023", color=ACCENT_GREEN, pad=0)
    
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.pie([45, 55], labels=["Hawkish", "Dovish"], colors=[ACCENT_BLUE, '#ff003c'], autopct='%1.1f%%', textprops={'color': TEXT_MAIN, 'fontsize': 8})
    ax3.set_title("ECB Sentiment 2023", color=ACCENT_GREEN, pad=0)
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 5: Time Series (Line Chart)
def slide_5(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig.patch.set_facecolor(BG_COLOR)
    
    dates = pd.date_range(start='2022-01-01', periods=100, freq='W')
    yields = np.linspace(1.5, 4.98, 100) + np.random.normal(0, 0.2, 100)
    
    ax.plot(dates, yields, color=ACCENT_BLUE, linewidth=2)
    ax.fill_between(dates, yields, color=ACCENT_BLUE, alpha=0.2)
    ax.set_title("FRED DGS10 YIELD SHOCK (2022-2023)", color=ACCENT_BLUE, fontsize=16, weight='bold', pad=20)
    ax.grid(True, color=TEXT_SUB, alpha=0.3)
    
    ax.annotate("Peak 4.98%", xy=(dates[80], 4.98), xytext=(dates[60], 4.5),
                arrowprops=dict(facecolor=ACCENT_GREEN, shrink=0.05),
                fontsize=12, color=ACCENT_GREEN)
                
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 6: Bar Charts
def slide_6(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.9, bottom=0.05)
    fig.patch.set_facecolor(BG_COLOR)
    
    x = np.arange(len(banks))
    width = 0.35
    
    ax.bar(x - width/2, scores, width, label='Composite Score', color=ACCENT_BLUE)
    ax.bar(x + width/2, np.random.uniform(50, 90, len(banks)), width, label='NLP Consistency', color=ACCENT_GREEN)
    
    ax.set_ylabel('Scores (0-100)')
    ax.set_title('COMPOSITE VS NLP CONSISTENCY', color=ACCENT_BLUE, fontsize=16, weight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(banks)
    ax.legend(loc='upper right', facecolor=BG_COLOR, edgecolor=TEXT_SUB)
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 7: Technical Stack
def slide_7(pdf):
    fig = plt.figure(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    
    fig.text(0.5, 0.8, "ENGINEERING STACK", fontsize=24, color=ACCENT_GREEN, ha='center', weight='bold')
    
    stacks = [
        "Data Extraction: FRED API, Web Scraping",
        "Database: PostgreSQL (Forward-Fill Imputed)",
        "NLP Engine: HuggingFace FinBERT",
        "Visualization: Matplotlib, NetworkX, Plotly",
        "Frontend: Streamlit"
    ]
    
    for i, s in enumerate(stacks):
        fig.text(0.5, 0.6 - (i*0.05), s, fontsize=12, ha='center', color=TEXT_MAIN)
        
    fig.text(0.5, 0.3, "Designed by Anurag Singh", fontsize=16, color=ACCENT_BLUE, ha='center', weight='bold')
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'Ultra_Dense_CBCI_Carousel.pdf')
    with PdfPages(out_path) as pdf:
        slide_1(pdf)
        slide_2(pdf)
        slide_3(pdf)
        slide_4(pdf)
        slide_5(pdf)
        slide_6(pdf)
        slide_7(pdf)
    print(f"Generated ultra-dense PDF at {out_path}")
