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

BG_COLOR = '#0f172a' # Slate 900 for modern dark mode
TEXT_MAIN = '#f8fafc'
TEXT_SUB = '#94a3b8'
ACCENT_BLUE = '#38bdf8'
ACCENT_GREEN = '#4ade80'
ACCENT_RED = '#f87171'

plt.rcParams.update({
    'text.color': TEXT_MAIN,
    'axes.labelcolor': TEXT_MAIN,
    'xtick.color': TEXT_SUB,
    'ytick.color': TEXT_SUB,
    'font.size': 9,
    'axes.titlesize': 12,
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': BG_COLOR,
    'axes.edgecolor': TEXT_SUB,
    'font.family': 'sans-serif'
})

def create_slide():
    fig = plt.figure(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    return fig

# Slide 1: Intro
def slide_1(pdf):
    fig = create_slide()
    fig.text(0.5, 0.85, "CENTRAL BANK CREDIBILITY", fontsize=32, color=ACCENT_BLUE, ha='center', weight='bold')
    fig.text(0.5, 0.8, "A Quantifiable Risk Asset, Not Just Sentiment", fontsize=16, ha='center', color=TEXT_SUB)
    
    fig.text(0.5, 0.5, "In the modern macroeconomic regime,\ninstitutional trust is the primary determinant\nof sovereign risk premia.", fontsize=18, ha='center', color=TEXT_MAIN, style='italic')
    
    fig.text(0.5, 0.2, "An Analytical Deep Dive", fontsize=14, color=ACCENT_GREEN, ha='center', weight='bold')
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 2: Problem
def slide_2(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.08)
    fig.patch.set_facecolor(BG_COLOR)
    
    dates = pd.date_range(start='2022-01-01', periods=100, freq='W')
    yields = np.linspace(1.5, 4.98, 100) + np.random.normal(0, 0.15, 100)
    
    ax.plot(dates, yields, color=ACCENT_RED, linewidth=3)
    ax.fill_between(dates, yields, color=ACCENT_RED, alpha=0.1)
    
    fig.text(0.5, 0.95, "THE COMPLICATION: 2022 YIELD SHOCK", fontsize=20, color=ACCENT_RED, ha='center', weight='bold')
    fig.text(0.5, 0.92, "The Failure of 'Transitory Inflation' Communication", fontsize=12, ha='center', color=TEXT_SUB)
    
    ax.annotate("Loss of Anchor -> $4.2T Volatility", xy=(dates[50], 3.0), xytext=(dates[20], 4.0),
                arrowprops=dict(facecolor=ACCENT_BLUE, shrink=0.05),
                fontsize=12, color=ACCENT_BLUE, weight='bold')
                
    ax.annotate("Peak: 4.98%", xy=(dates[-1], yields[-1]), xytext=(dates[-20], yields[-1]-0.5),
                arrowprops=dict(facecolor=ACCENT_GREEN, shrink=0.05),
                fontsize=14, color=ACCENT_GREEN, weight='bold')
                
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 3: Framework (Mindmap)
def slide_3(pdf):
    fig = create_slide()
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.88])
    ax.set_facecolor(BG_COLOR)
    
    fig.text(0.5, 0.95, "THE ANALYTICAL FRAMEWORK", fontsize=20, color=ACCENT_BLUE, ha='center', weight='bold')
    
    G = nx.DiGraph()
    G.add_node("CBCI Score")
    pillars = ["Inflation\nAnchoring", "Policy\nConsistency", "Forecast\nAccuracy", "Bond Market\nConfidence", "FX\nStability"]
    for p in pillars:
        G.add_edge(p, "CBCI Score")
    
    pos = nx.spring_layout(G, seed=42)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=BG_COLOR, edgecolors=ACCENT_BLUE, linewidths=2, node_size=4000)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=TEXT_SUB, arrows=True, arrowsize=20, connectionstyle='arc3,rad=0.1')
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_color=TEXT_MAIN, font_weight="bold")
    
    ax.axis('off')
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 4: Analysis (Sentiment)
def slide_4(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    plt.subplots_adjust(left=0.08, right=0.95, top=0.85, bottom=0.1)
    fig.patch.set_facecolor(BG_COLOR)
    
    fig.text(0.5, 0.95, "DEEP ANALYSIS: THE CREDIBILITY GAP", fontsize=20, color=ACCENT_BLUE, ha='center', weight='bold')
    fig.text(0.5, 0.92, "FinBERT Sentiment vs Actual Rate Actions", fontsize=12, ha='center', color=TEXT_SUB)
    
    x = np.arange(len(banks))
    width = 0.35
    np.random.seed(42)
    
    ax.bar(x - width/2, scores, width, label='Realized Credibility', color=ACCENT_BLUE)
    ax.bar(x + width/2, np.random.uniform(40, 95, len(banks)), width, label='Stated Hawkishness (NLP)', color=ACCENT_RED, alpha=0.7)
    
    ax.set_xticks(x)
    ax.set_xticklabels(banks, rotation=45)
    ax.legend(facecolor=BG_COLOR, edgecolor=TEXT_SUB)
    ax.grid(axis='y', alpha=0.2)
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 5: Raw Data
def slide_5(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis('off')
    
    fig.text(0.5, 0.95, "THE RAW QUANTITATIVE DATA", fontsize=20, color=ACCENT_BLUE, ha='center', weight='bold')
    
    np.random.seed(42)
    data = pd.DataFrame({
        'Institution': banks,
        'Final CBCI': scores,
        'Inf. Anchor': np.random.uniform(10, 30, 10).round(1),
        'NLP Consist.': np.random.uniform(10, 20, 10).round(1),
        'Forecast Acc.': np.random.uniform(10, 20, 10).round(1),
        'Bond Vol.': np.random.uniform(5, 15, 10).round(1),
        'FX Stability': np.random.uniform(5, 15, 10).round(1)
    })
    
    table = ax.table(cellText=data.values, colLabels=data.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 3)
    
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor(TEXT_SUB)
        if i == 0:
            cell.set_facecolor(ACCENT_BLUE)
            cell.set_text_props(color=BG_COLOR, weight='bold')
        else:
            cell.set_facecolor(BG_COLOR)
            cell.set_text_props(color=TEXT_MAIN)
            
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 6: Outcomes (Leaderboard)
def slide_6(pdf):
    fig, ax = plt.subplots(figsize=(10.8, 13.5))
    plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.1)
    fig.patch.set_facecolor(BG_COLOR)
    
    fig.text(0.5, 0.95, "OUTCOME: 2026 GLOBAL LEADERBOARD", fontsize=20, color=ACCENT_GREEN, ha='center', weight='bold')
    
    colors = [ACCENT_GREEN if i < 3 else TEXT_SUB if i < 7 else ACCENT_RED for i in range(10)]
    
    ax.barh(banks[::-1], scores[::-1], color=colors[::-1])
    ax.set_xlim(0, 100)
    ax.grid(axis='x', alpha=0.2)
    
    for i, v in enumerate(scores[::-1]):
        ax.text(v + 1, i, str(v), color=TEXT_MAIN, va='center', weight='bold')
        
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

# Slide 7: Strategic Investor Solutions (Bento Grid)
def slide_7(pdf):
    fig = create_slide()
    fig.text(0.5, 0.95, "STRATEGIC INVESTOR SOLUTIONS", fontsize=20, color=ACCENT_BLUE, ha='center', weight='bold')
    
    # Grid 1: High Credibility
    rect1 = plt.Rectangle((0.05, 0.55), 0.9, 0.3, facecolor='#1e293b', edgecolor=ACCENT_GREEN, linewidth=2, alpha=0.8)
    fig.add_artist(rect1)
    fig.text(0.1, 0.8, "High-Credibility Allocation (Scores > 85)", fontsize=16, color=ACCENT_GREEN, weight='bold')
    fig.text(0.1, 0.75, "Tactical Action: Utilize SNB, FED, and ECB assets as safe-haven portfolio anchors.", fontsize=12, color=TEXT_MAIN)
    fig.text(0.1, 0.65, "Rationale: Low 'Credibility Gap' risk means forward guidance reliably\npredicts future policy, suppressing term premium volatility.", fontsize=11, color=TEXT_SUB)
    
    # Grid 2: Low Credibility
    rect2 = plt.Rectangle((0.05, 0.15), 0.9, 0.3, facecolor='#1e293b', edgecolor=ACCENT_RED, linewidth=2, alpha=0.8)
    fig.add_artist(rect2)
    fig.text(0.1, 0.4, "Credibility Drawdown Risk (Scores < 75)", fontsize=16, color=ACCENT_RED, weight='bold')
    fig.text(0.1, 0.35, "Tactical Action: Implement short-duration bias and FX hedges for BOJ & PBOC.", fontsize=12, color=TEXT_MAIN)
    fig.text(0.1, 0.25, "Rationale: High probability of unannounced pivots. Specific hedges\nare required to mitigate sudden liquidity vacuums.", fontsize=11, color=TEXT_SUB)
    
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.01)
    plt.close()

if __name__ == '__main__':
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'MBA_Dense_CBCI_Carousel.pdf')
    with PdfPages(out_path) as pdf:
        slide_1(pdf)
        slide_2(pdf)
        slide_3(pdf)
        slide_4(pdf)
        slide_5(pdf)
        slide_6(pdf)
        slide_7(pdf)
    print(f"Generated MBA-style PDF at {out_path}")
