import os
import textwrap
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
df_scores = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'final_cbci_scores.csv'))
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
    title=dict(text="Global Central Bank Credibility Index (CBCI) - Methodological Breakdown", font=dict(size=24, family='Inter'), x=0.5),
    barmode='stack',
    font=dict(family='Inter'),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False),
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

fig2.add_vrect(x0="2020-03-01", x1="2021-06-01", fillcolor="#EF4444", opacity=0.3, layer="below", line_width=0)
fig2.add_vrect(x0="2022-03-01", x1="2023-12-31", fillcolor="#3B82F6", opacity=0.3, layer="below", line_width=0)
# Dummy traces for legend
fig2.add_trace(go.Bar(x=[None], y=[None], name='Pandemic Shock / ZIRP', marker_color='rgba(239, 68, 68, 0.5)'))
fig2.add_trace(go.Bar(x=[None], y=[None], name='Aggressive Hiking Cycle', marker_color='rgba(59, 130, 246, 0.5)'))

# Annotation for Peak
peak_row = df_macro.loc[df_macro['value'].idxmax()]
peak_date_str = peak_row['date'].strftime('%Y-%m-%d')
fig2.add_annotation(x=peak_date_str, y=peak_row['value'], text="Terminal Rate Peak: 4.98%<br>Oct 2023", 
                    showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='#EF4444',
                    bordercolor='#EF4444', borderwidth=1, bgcolor='#2A0A0A', font=dict(color='#EF4444', size=14), ax=-60, ay=10)

fig2.add_trace(go.Scatter(x=[peak_date_str], y=[peak_row['value']], mode='markers', name='', showlegend=False, marker=dict(color='#EF4444', size=10)))

fig2.update_layout(
    title=dict(text="Macro Policy Shock Monitor: 10-Year Treasury Yield Dynamics", font=dict(size=24, family='Inter'), x=0.5),
    font=dict(family='Inter'),
    yaxis_title="Yield (%)", xaxis_title="Timeline (2010 - 2026)",
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor='#1E293B'),
    margin=dict(l=40, r=40, t=60, b=40),
    paper_bgcolor='#0B0F19', plot_bgcolor='#0B0F19',
    legend=dict(x=0.01, y=0.99, bgcolor='rgba(11,15,25,0.8)', bordercolor='#334155', borderwidth=1)
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

def draw_wrapped_text(canvas_obj, text, x, y, font, size, color, max_width_chars=45, line_height=None):
    if line_height is None:
        line_height = size * 1.3
    canvas_obj.setFont(font, size)
    canvas_obj.setFillColor(color)
    lines = textwrap.wrap(text, width=max_width_chars)
    for line in lines:
        canvas_obj.drawString(x, y, line)
        y -= line_height
    return y

# SLIDE 1: Intro
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1150, "PROJECT OVERVIEW")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 90)
c.drawString(80, 1020, "The Central Bank")
c.drawString(80, 910, "Credibility Index")

y = 780
y = draw_wrapped_text(c, "The 2022 global inflation crisis served as a watershed moment for modern monetary policy.", 80, y, f_reg, 36, TEXT_SEC, 48)
y -= 40
y = draw_wrapped_text(c, "The 'Transitory Inflation' narrative was a strategic miscalculation that led to a total breakdown in forward guidance, stripping markets of their primary navigational tools.", 80, y, f_reg, 36, TEXT_SEC, 48)
y -= 40
y = draw_wrapped_text(c, "To mitigate these risks, the CBCI was developed as a rigorous, data-driven framework to quantify institutional trust and extract asymmetric insights from policy behavior.", 80, y, f_reg, 36, TEXT_SEC, 48)
c.showPage()

# SLIDE 2: Framework
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "01 / THE FRAMEWORK")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "The 5-Pillar Model")
y = draw_wrapped_text(c, "To ensure a definitive 0-100 credibility score insulated from bias:", 80, 980, f_reg, 34, TEXT_SEC, 50)
y -= 40

pillars_desc = [
    ("1. Inflation Anchoring (30%)", "Measures absolute deviation of headline inflation from official targets over a 12-month window."),
    ("2. Policy Consistency (20%)", "Evaluates NLP alignment between communication (FinBERT) and subsequent interest rate moves."),
    ("3. Forecast Accuracy (20%)", "Quantifies Mean Absolute Error (MAE) of the central bank's own economic projections."),
    ("4. Bond Confidence (15%)", "Tracks rolling volatility in sovereign bonds (utilizing FRED DGS10 data)."),
    ("5. FX Stability (15%)", "Evaluates currency pair stability and safe-haven behavior during market stress.")
]
for title, desc in pillars_desc:
    c.setFillColor(HexColor('#1E293B'))
    c.roundRect(80, y - 90, 920, 130, 15, fill=1, stroke=0)
    c.setFillColor(TEXT_PRI)
    c.setFont(f_bold, 30)
    c.drawString(110, y - 10, title)
    draw_wrapped_text(c, desc, 110, y - 55, f_reg, 26, ACCENT_GRN, 60)
    y -= 150
c.showPage()

# SLIDE 3: Data Architecture
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "02 / ENTERPRISE ARCHITECTURE")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Data Engineering")
y = draw_wrapped_text(c, "A strategic shift from fragile manual spreadsheets to an automated, high-integrity pipeline.", 80, 960, f_reg, 34, TEXT_SEC, 50)
y -= 60

y = draw_wrapped_text(c, "⚙️ Python & Pandas (ETL)", 80, y, f_bold, 38, TEXT_PRI, 50)
y = draw_wrapped_text(c, "Ingesting over 4,200 days of raw data directly from the FRED API. Eliminates human error.", 80, y-10, f_reg, 34, TEXT_SEC, 50)
y -= 60

y = draw_wrapped_text(c, "🗄️ Relational Integrity (PostgreSQL)", 80, y, f_bold, 38, TEXT_PRI, 50)
y = draw_wrapped_text(c, "The single source of truth. Enforcing strict data types and managing exact FOMC meeting metadata.", 80, y-10, f_reg, 34, TEXT_SEC, 50)
y -= 60

y = draw_wrapped_text(c, "📊 Code-as-UI (Streamlit)", 80, y, f_bold, 38, TEXT_PRI, 50)
y = draw_wrapped_text(c, "Moving away from unversioned drag-and-drop tools to fully auditable, Git-versioned visualization layers.", 80, y-10, f_reg, 34, TEXT_SEC, 50)

c.showPage()

# SLIDE 4: NLP
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "03 / THE INNOVATION")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Objective NLP Sentiment")

y = draw_wrapped_text(c, "A central innovation of the CBCI is the use of Natural Language Processing (NLP) to convert unstructured central bank communications into quantitative data points.", 80, 960, f_reg, 34, TEXT_SEC, 50)
y -= 60

y = draw_wrapped_text(c, "🧠 The FinBERT Model", 80, y, f_bold, 38, TEXT_PRI, 50)
y = draw_wrapped_text(c, "Specifically trained for financial contexts. FinBERT parses thousands of FOMC and ECB policy statements to generate a precise hawkish-dovish scale.", 80, y-10, f_reg, 34, TEXT_SEC, 50)
y -= 60

y = draw_wrapped_text(c, "⚡ The 'Policy Shock' Metric", 80, y, f_bold, 38, TEXT_PRI, 50)
y = draw_wrapped_text(c, "The model heavily penalizes central banks when dovish communication is immediately followed by hawkish actions. These shocks are a primary driver of catastrophic bond market volatility.", 80, y-10, f_reg, 34, TEXT_SEC, 50)

c.showPage()

# SLIDE 5: Outcome
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "04 / THE OUTCOME")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Global Leaderboard")

c.drawImage(chart1_path, 80, 430, 920, 580, mask='auto')

y = 350
y = draw_wrapped_text(c, "🏆 The Gold Standard: SNB (89.4)", 80, y, f_bold, 36, TEXT_PRI, 50)
y = draw_wrapped_text(c, "Maintained extreme FX stability and tight inflation anchoring throughout the 2020s.", 80, y-10, f_reg, 30, TEXT_SEC, 55)
y -= 40
y = draw_wrapped_text(c, "⚠️ Critical Laggard: PBOC (59.8)", 80, y, f_bold, 36, TEXT_PRI, 50)
y = draw_wrapped_text(c, "Penalized for lack of transparent forward guidance and policy consistency.", 80, y-10, f_reg, 30, TEXT_SEC, 55)
c.showPage()

# SLIDE 6: Macro Shock
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "05 / MACRO SHOCK MONITOR")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Treasury Yield Dynamics")

c.drawImage(chart2_path, 80, 550, 920, 480, mask='auto')

y = 480
y = draw_wrapped_text(c, "Final Takeaways for Audit & Oversight", 80, y, f_bold, 38, TEXT_PRI, 50)
y -= 20
y = draw_wrapped_text(c, "• Engineering Over Manual Logic: Transitioning to Python/SQL is essential for mitigating model risk.", 80, y, f_reg, 30, TEXT_SEC, 55)
y -= 10
y = draw_wrapped_text(c, "• Sentiment as a Hard Metric: NLP models turn rhetoric into tradable, measurable signals.", 80, y, f_reg, 30, TEXT_SEC, 55)
y -= 10
y = draw_wrapped_text(c, "• Consistency is the Asset: Credibility is the alignment of words, forecasts, and actions.", 80, y, f_reg, 30, TEXT_SEC, 55)

y -= 40
draw_wrapped_text(c, "\"In the modern financial landscape, trust is the most volatile asset of all. Rebuilding market trust takes years, but losing it takes only one missed forecast.\"", 80, y, f_bold, 30, ACCENT_BLU, 55)

c.showPage()
c.save()
print('Successfully generated wrapped CBCI Whitepaper Carousel!')
