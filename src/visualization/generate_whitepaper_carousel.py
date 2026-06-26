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


# --- CHART 3: Global Credibility Map ---
bank_coords = {
    'SNB': (46.8, 8.2, 'Switzerland'), 'FED': (38.9, -77.0, 'USA'),
    'ECB': (50.1, 8.6, 'Eurozone'), 'BOE': (51.5, -0.1, 'UK'),
    'BOC': (45.4, -75.7, 'Canada'), 'RBA': (-35.3, 149.1, 'Australia'),
    'BOJ': (35.6, 139.6, 'Japan'), 'BCB': (-15.8, -47.9, 'Brazil'),
    'RBI': (19.0, 72.8, 'India'), 'PBOC': (39.9, 116.4, 'China')
}

df_map = df_scores.copy()
df_map['Lat'] = df_map['Central Bank'].map(lambda x: bank_coords[x][0])
df_map['Lon'] = df_map['Central Bank'].map(lambda x: bank_coords[x][1])
df_map['Country'] = df_map['Central Bank'].map(lambda x: bank_coords[x][2])
df_map['Label'] = df_map['Central Bank'] + ": " + df_map['Total Score'].astype(str)

fig3 = go.Figure(data=go.Scattergeo(
    lon=df_map['Lon'],
    lat=df_map['Lat'],
    text=df_map['Label'],
    mode='markers+text',
    textposition="top center",
    textfont=dict(family='Inter', size=16, color='white'),
    marker=dict(
        size=df_map['Total Score'] / 3,
        color=df_map['Total Score'],
        colorscale='RdYlGn',
        cmin=50, cmax=90,
        showscale=True,
        colorbar=dict(title=dict(text="CBCI Score", font=dict(color='white')), tickfont=dict(color='white')),
        line=dict(width=1, color='white')
    )
))

fig3.update_layout(
    title=dict(text="Global Credibility Heatmap", font=dict(size=24, family='Inter', color='white'), x=0.5),
    geo=dict(
        showframe=False,
        showcoastlines=True, coastlinecolor="#334155",
        showland=True, landcolor="#0f172a",
        showocean=True, oceancolor="#0B0F19",
        showcountries=True, countrycolor="#1E293B",
        bgcolor='#0B0F19',
        projection_type='equirectangular'
    ),
    paper_bgcolor='#0B0F19',
    plot_bgcolor='#0B0F19',
    margin=dict(l=0, r=0, t=60, b=0)
)
chart3_path = os.path.join(img_dir, 'chart3_map.png')
fig3.write_image(chart3_path, width=1200, height=600)

# --- CHART 4: Policy vs Action Matrix (Bubble) ---
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=df_scores['Policy Consistency (20%)'],
    y=df_scores['Inflation Anchoring (30%)'],
    mode='markers+text',
    text=df_scores['Central Bank'],
    textposition="top center",
    textfont=dict(family='Inter', size=14, color='white'),
    marker=dict(
        size=df_scores['Total Score'],
        sizemode='area',
        sizeref=2.*max(df_scores['Total Score'])/(50.**2),
        color=df_scores['Total Score'],
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(title=dict(text="CBCI Score", font=dict(color='white')), tickfont=dict(color='white')),
        line=dict(width=2, color='white')
    )
))

x_mid = df_scores['Policy Consistency (20%)'].mean()
y_mid = df_scores['Inflation Anchoring (30%)'].mean()
fig4.add_vline(x=x_mid, line_dash="dash", line_color="#94A3B8")
fig4.add_hline(y=y_mid, line_dash="dash", line_color="#94A3B8")

fig4.add_annotation(x=x_mid + 2, y=y_mid + 3, text="Strong Anchors & Consistency", showarrow=False, font=dict(color="#10B981", size=14))
fig4.add_annotation(x=x_mid - 2, y=y_mid - 3, text="Weak Anchors & Consistency", showarrow=False, font=dict(color="#EF4444", size=14))

fig4.update_layout(
    title=dict(text="Policy vs Action Matrix", font=dict(size=24, family='Inter', color='white'), x=0.5),
    xaxis_title="Policy Consistency Score (Max 20)",
    yaxis_title="Inflation Anchoring Score (Max 30)",
    font=dict(family='Inter', color='white'),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(gridcolor='#1E293B', zeroline=False),
    paper_bgcolor='#0B0F19',
    plot_bgcolor='#0B0F19',
    margin=dict(l=40, r=40, t=60, b=40)
)
chart4_path = os.path.join(img_dir, 'chart4_bubble.png')
fig4.write_image(chart4_path, width=1200, height=600)

# --- CHART 5: Credibility Anatomy (Radar) ---
categories = ['Inflation Anchoring (30%)', 'Policy Consistency (20%)', 'Forecast Accuracy (20%)', 'Bond Confidence (15%)', 'FX Stability (15%)']
fig5 = go.Figure()
for bank, color in zip(['SNB', 'FED', 'PBOC'], ['#10B981', '#3B82F6', '#EF4444']):
    bank_data = df_scores[df_scores['Central Bank'] == bank].iloc[0]
    max_scores = [30.0, 20.0, 20.0, 15.0, 15.0]
    values = [bank_data[cat]/mx * 100 for cat, mx in zip(categories, max_scores)]
    values.append(values[0])
    cat_closed = [c.split(' (')[0] for c in categories] + [categories[0].split(' (')[0]]
    fig5.add_trace(go.Scatterpolar(
        r=values,
        theta=cat_closed,
        fill='toself',
        name=bank,
        line_color=color,
        opacity=0.6
    ))
fig5.update_layout(
    title=dict(text="Credibility Anatomy: % of Max Potential Achieved", font=dict(size=24, family='Inter', color='white'), x=0.5),
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor='#334155', linecolor='#334155', tickfont=dict(color='#94A3B8')),
        angularaxis=dict(gridcolor='#334155', linecolor='#334155', tickfont=dict(color='white', size=16)),
        bgcolor='#0B0F19'
    ),
    font=dict(family='Inter', color='white'),
    paper_bgcolor='#0B0F19',
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=16)),
    margin=dict(l=80, r=80, t=80, b=80)
)
chart5_path = os.path.join(img_dir, 'chart5_radar.png')
fig5.write_image(chart5_path, width=1200, height=700)

# --- CHART 6: Volatility Heatmap ---
# Calculate rolling 30-day volatility of the 10-Year yield
df_macro['volatility'] = df_macro['value'].rolling(window=30).std()
# Create a monthly aggregated heatmap
df_macro['year_month'] = df_macro['date'].dt.to_period('M')
df_heatmap = df_macro.groupby('year_month')['volatility'].mean().reset_index()
df_heatmap['year'] = df_heatmap['year_month'].dt.year
df_heatmap['month'] = df_heatmap['year_month'].dt.month
pivot = df_heatmap.pivot(index='year', columns='month', values='volatility')

fig6 = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    y=pivot.index,
    colorscale='Reds',
    colorbar=dict(title=dict(text="Volatility (std dev)", font=dict(color='white')), tickfont=dict(color='white'))
))
fig6.update_layout(
    title=dict(text="Macro Shock Intensity: 10-Year Treasury Yield Volatility", font=dict(size=24, family='Inter', color='white'), x=0.5),
    font=dict(family='Inter', color='white'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False, autorange="reversed"),
    paper_bgcolor='#0B0F19',
    plot_bgcolor='#0B0F19',
    margin=dict(l=40, r=40, t=60, b=40)
)
chart6_path = os.path.join(img_dir, 'chart6_heatmap.png')
fig6.write_image(chart6_path, width=1200, height=600)

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

def draw_slide_header(canvas_obj, tag, title, color=ACCENT_BLU):
    canvas_obj.setFillColor(color)
    canvas_obj.setFont(f_bold, 32)
    canvas_obj.drawString(80, 1200, tag)
    canvas_obj.setFillColor(TEXT_PRI)
    canvas_obj.setFont(f_bold, 70)
    canvas_obj.drawString(80, 1100, title)

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

# SLIDE 5: Map
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "04 / GEOGRAPHIC CONTEXT")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Global Credibility Heatmap")
c.drawImage(chart3_path, 80, 550, 920, 480, mask='auto')
y = 500
c.setFillColor(HexColor('#1E293B'))
c.roundRect(80, y - 140, 920, 140, 15, fill=1, stroke=0)
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 34)
c.drawString(110, y - 40, "🌍 The Analyst Insight")
draw_wrapped_text(c, "Institutional trust is heavily concentrated in Western European and North American hubs, showing strong structural resilience compared to emerging markets and heavily opaque regimes.", 110, y - 80, f_reg, 26, TEXT_PRI, 60)
c.showPage()

# SLIDE 6: Outcome
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "05 / THE OUTCOME")
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

# SLIDE 7: Policy vs Action
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "06 / ADVANCED ANALYTICS")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Policy vs Action Matrix")
c.drawImage(chart4_path, 80, 430, 920, 580, mask='auto')
c.showPage()

# SLIDE 8: Radar Chart
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "07 / ADVANCED ANALYTICS")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Credibility Anatomy")
c.drawImage(chart5_path, 80, 350, 920, 680, mask='auto')
c.showPage()

# SLIDE 9: Macro Shock
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "08 / MACRO SHOCK MONITOR")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Treasury Yield Dynamics")
c.drawImage(chart2_path, 80, 550, 920, 480, mask='auto')
y = 480
y = draw_wrapped_text(c, "Market memory is short, but the bond market always remembers.", 80, y, f_bold, 38, TEXT_PRI, 50)
c.showPage()

# SLIDE 10: Volatility Heatmap
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "09 / MACRO SHOCK MONITOR")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Yield Volatility Heatmap")
c.drawImage(chart6_path, 80, 430, 920, 580, mask='auto')
c.showPage()

# SLIDE 11: Final Takeaways
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 32)
c.drawString(80, 1200, "10 / CONCLUSION")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 70)
c.drawString(80, 1080, "Final Takeaways for Audit")
y = 900
y = draw_wrapped_text(c, "• Engineering Over Manual Logic: Transitioning to Python/SQL is essential for mitigating model risk.", 80, y, f_reg, 34, TEXT_SEC, 55)
y -= 40
y = draw_wrapped_text(c, "• Sentiment as a Hard Metric: NLP models turn rhetoric into tradable, measurable signals.", 80, y, f_reg, 34, TEXT_SEC, 55)
y -= 40
y = draw_wrapped_text(c, "• Consistency is the Asset: Credibility is the alignment of words, forecasts, and actions.", 80, y, f_reg, 34, TEXT_SEC, 55)
y -= 80
draw_wrapped_text(c, "\"In the modern financial landscape, trust is the most volatile asset of all. Rebuilding market trust takes years, but losing it takes only one missed forecast.\"", 80, y, f_bold, 34, ACCENT_BLU, 55)
c.showPage()
c.save()
print('Successfully generated wrapped CBCI Whitepaper Carousel!')
