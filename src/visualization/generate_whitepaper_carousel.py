import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
out_dir = os.path.join(base_dir, 'docs')
img_dir = os.path.join(out_dir, 'temp_images')
os.makedirs(img_dir, exist_ok=True)

# Fonts
try:
    pdfmetrics.registerFont(TTFont('Inter', 'C:\\Windows\\Fonts\\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
    f_reg, f_bold = 'Inter', 'Inter-Bold'
except:
    f_reg, f_bold = 'Helvetica', 'Helvetica-Bold'

# Load Data
df_scores = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'authentic_cbci_scores.csv'))
df_macro = pd.read_csv(os.path.join(base_dir, 'data', 'raw', 'fred_dgs10.csv'))

# --- CHART 1: Stacked Bar Leaderboard ---
pio.templates.default = "plotly_dark"
df_scores_sorted = df_scores.sort_values('Total Score', ascending=True)

fig1 = go.Figure()
colors = ['#22C55E', '#3B82F6', '#A855F7', '#C084FC', '#FF8A65']
pillars = ['Inflation Anchoring (30%)', 'Policy Consistency (20%)', 'Forecast Accuracy (20%)', 'Bond Confidence (15%)', 'FX Stability (15%)']

for i, pillar in enumerate(pillars):
    fig1.add_trace(go.Bar(
        y=df_scores_sorted['Central Bank'],
        x=df_scores_sorted[pillar],
        name=pillar,
        orientation='h',
        marker=dict(color=colors[i], line=dict(color='black', width=1))
    ))

# Add annotations for total score
for i, row in df_scores_sorted.iterrows():
    fig1.add_annotation(
        x=row['Total Score'] + 2, y=row['Central Bank'],
        text=f"<b>{row['Total Score']}</b>", showarrow=False, font=dict(size=18, color='white')
    )

fig1.update_layout(
    title=dict(text="Global Central Bank Credibility Index (CBCI) - Methodological Breakdown", font=dict(size=24), x=0.5),
    barmode='stack',
    margin=dict(l=40, r=40, t=60, b=100),
    paper_bgcolor='#0B0F19', plot_bgcolor='#0B0F19',
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=14))
)
chart1_path = os.path.join(img_dir, 'chart1_stacked.png')
fig1.write_image(chart1_path, width=1200, height=700)

# --- CHART 2: Macro Policy Shock Monitor ---
df_macro['date'] = pd.to_datetime(df_macro['date'], errors='coerce')
df_macro['value'] = pd.to_numeric(df_macro['value'], errors='coerce')
df_macro = df_macro.dropna().sort_values('date')
df_macro['SMA_50'] = df_macro['value'].rolling(window=50).mean()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_macro['date'], y=df_macro['value'], mode='lines', name='10-Year Treasury Yield (DGS10)', line=dict(color='#3B82F6', width=1.5)))
fig2.add_trace(go.Scatter(x=df_macro['date'], y=df_macro['SMA_50'], mode='lines', name='50-Day Moving Average', line=dict(color='#EF4444', width=1.5, dash='dash')))

# Shaded regions
fig2.add_vrect(x0="2020-03-01", x1="2021-06-01", fillcolor="red", opacity=0.1, layer="below", line_width=0, name='Pandemic Shock / ZIRP')
fig2.add_vrect(x0="2022-03-01", x1="2023-12-31", fillcolor="blue", opacity=0.1, layer="below", line_width=0, name='Aggressive Hiking Cycle')

# Annotation for Peak
peak_row = df_macro.loc[df_macro['value'].idxmax()]
fig2.add_annotation(x=peak_row['date'], y=peak_row['value'], text="Terminal Rate Peak: 4.98%<br>Oct 2023", 
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#EF4444',
                    bordercolor='#EF4444', borderwidth=1, bgcolor='#2A0A0A', font=dict(color='#EF4444', size=14), ax=-60, ay=10)

fig2.add_trace(go.Scatter(x=[peak_row['date']], y=[peak_row['value']], mode='markers', name='', showlegend=False, marker=dict(color='#EF4444', size=10)))

fig2.update_layout(
    title=dict(text="Macro Policy Shock Monitor: 10-Year Treasury Yield Dynamics", font=dict(size=24), x=0.5),
    yaxis_title="Yield (%)", xaxis_title="Timeline (2010 - 2026)",
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='#0B0F19', plot_bgcolor='#0B0F19',
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(0,0,0,0.5)')
)
chart2_path = os.path.join(img_dir, 'chart2_macro.png')
fig2.write_image(chart2_path, width=1200, height=600)

# --- GENERATE PDF CAROUSEL ---
pdf_path = os.path.join(out_dir, 'CBCI_Whitepaper_Carousel.pdf')
c = canvas.Canvas(pdf_path, pagesize=(1080, 1350))

BG_COLOR = HexColor('#0B0F19')
TEXT_PRI = HexColor('#F8FAFC')
TEXT_SEC = HexColor('#94A3B8')
ACCENT_BLU = HexColor('#3B82F6')
ACCENT_GRN = HexColor('#10B981')

def draw_bg():
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, 1080, 1350, fill=1, stroke=0)

# SLIDE 1
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1150, "PROJECT OVERVIEW")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 100)
c.drawString(80, 1000, "The Central Bank")
c.drawString(80, 880, "Credibility Index")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 40)
text1 = [
    "The 2022 global inflation crisis served as a watershed moment",
    "for modern monetary policy.",
    "",
    "The 'Transitory Inflation' narrative was a strategic miscalculation",
    "that led to a total breakdown in forward guidance, stripping",
    "markets of their primary navigational tools.",
    "",
    "To mitigate these risks, the CBCI was developed as a rigorous,",
    "data-driven framework to quantify institutional trust and extract",
    "asymmetric insights from policy behavior."
]
y = 750
for line in text1:
    if line == "": y -= 30; continue
    c.drawString(80, y, line)
    y -= 50
c.showPage()

# SLIDE 2
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "01 / THE FRAMEWORK")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "The 5-Pillar Model")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 36)
c.drawString(80, 950, "To ensure a definitive 0-100 credibility score insulated from bias:")

pillars_desc = [
    ("1. Inflation Anchoring (30%)", "Deviation from targets over 12m window."),
    ("2. Policy Consistency (20%)", "NLP alignment of words vs interest rate moves."),
    ("3. Forecast Accuracy (20%)", "Mean Absolute Error of central bank projections."),
    ("4. Bond Confidence (15%)", "Rolling volatility in sovereign bonds (FRED DGS10)."),
    ("5. FX Stability (15%)", "Currency pair safe-haven behavior in stress.")
]
y = 800
for title, desc in pillars_desc:
    c.setFillColor(HexColor('#1E293B'))
    c.roundRect(80, y - 60, 920, 90, 15, fill=1, stroke=0)
    c.setFillColor(TEXT_PRI)
    c.setFont(f_bold, 32)
    c.drawString(110, y - 10, title)
    c.setFillColor(ACCENT_GRN)
    c.setFont(f_reg, 28)
    c.drawString(110, y - 45, desc)
    y -= 110
c.showPage()

# SLIDE 3
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "02 / ENTERPRISE ARCHITECTURE")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Data Engineering")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 38)
text3 = [
    "A strategic shift from fragile manual spreadsheets to an automated,",
    "high-integrity pipeline.",
    "",
    "⚙️ Python & Pandas (ETL)",
    "Ingesting over 4,200 days of raw data from the FRED API.",
    "",
    "🗄️ Relational Integrity (PostgreSQL)",
    "The single source of truth. Enforcing strict data types and",
    "managing exact FOMC meeting metadata.",
    "",
    "📊 Code-as-UI (Streamlit)",
    "Moving away from unversioned drag-and-drop tools to",
    "fully auditable, Git-versioned visualization layers."
]
y = 920
for line in text3:
    if line == "": y -= 30; continue
    if line.startswith("⚙️") or line.startswith("🗄️") or line.startswith("📊"):
        c.setFillColor(TEXT_PRI)
        c.setFont(f_bold, 42)
    else:
        c.setFillColor(TEXT_SEC)
        c.setFont(f_reg, 36)
    c.drawString(80, y, line)
    y -= 50
c.showPage()

# SLIDE 4
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "03 / THE INNOVATION")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Objective NLP Sentiment")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 38)
text4 = [
    "A central innovation of the CBCI is the use of Natural",
    "Language Processing (NLP) to convert unstructured central",
    "bank communications into quantitative data.",
    "",
    "🧠 The FinBERT Model",
    "Specifically trained for financial contexts, parsing thousands",
    "of FOMC statements to generate a precise hawkish-dovish scale.",
    "",
    "⚡ The 'Policy Shock' Metric",
    "The model heavily penalizes central banks when dovish",
    "communication is immediately followed by hawkish rate hikes.",
    "These shocks are a primary driver of bond volatility."
]
y = 920
for line in text4:
    if line == "": y -= 30; continue
    if line.startswith("🧠") or line.startswith("⚡"):
        c.setFillColor(TEXT_PRI)
        c.setFont(f_bold, 42)
    else:
        c.setFillColor(TEXT_SEC)
        c.setFont(f_reg, 36)
    c.drawString(80, y, line)
    y -= 50
c.showPage()

# SLIDE 5
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "04 / THE OUTCOME")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Global Leaderboard")

c.drawImage(chart1_path, 80, 400, 920, 600, mask='auto')

c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 38)
c.drawString(80, 320, "🏆 The Gold Standard: SNB (89.4)")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 32)
c.drawString(80, 270, "Maintained extreme FX stability and tight inflation anchoring.")

c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 38)
c.drawString(80, 180, "⚠️ The Laggards: PBOC & BOJ")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 32)
c.drawString(80, 130, "Penalized for lack of transparent guidance and YCC breakdown.")
c.showPage()

# SLIDE 6
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "05 / MACRO SHOCK MONITOR")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Treasury Yield Dynamics")

c.drawImage(chart2_path, 80, 520, 920, 480, mask='auto')

c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 42)
c.drawString(80, 420, "Final Takeaways for Audit & Oversight")

c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 34)
text6 = [
    "• Engineering Over Manual Logic: Transitioning to Python/SQL",
    "  is essential for mitigating model risk.",
    "• Sentiment as a Hard Metric: NLP models turn rhetoric",
    "  into tradable, measurable signals.",
    "• Consistency is the Asset: Credibility is the alignment of",
    "  words, forecasts, and actions."
]
y = 350
for line in text6:
    c.drawString(80, y, line)
    y -= 45

c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 100, "\"Trust is volatile. Rebuilding takes years, losing it takes one forecast.\"")

c.showPage()
c.save()
print('Successfully generated CBCI Whitepaper Carousel!')
