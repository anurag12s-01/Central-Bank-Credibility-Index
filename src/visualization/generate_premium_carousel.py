import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
out_dir = os.path.join(base_dir, 'docs')
img_dir = os.path.join(base_dir, 'docs', 'temp_images')
os.makedirs(img_dir, exist_ok=True)

# Try registering fonts
try:
    pdfmetrics.registerFont(TTFont('Inter', 'C:\\Windows\\Fonts\\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
    f_reg, f_bold = 'Inter', 'Inter-Bold'
except:
    f_reg, f_bold = 'Helvetica', 'Helvetica-Bold'

# Colors
BG_COLOR = HexColor('#0B0F19')
TEXT_PRI = HexColor('#F8FAFC')
TEXT_SEC = HexColor('#94A3B8')
ACCENT_BLU = HexColor('#3B82F6')
ACCENT_GRN = HexColor('#10B981')

# Data
df = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'authentic_cbci_scores.csv'))

# 1. Generate Plotly Charts & Save as Images
pio.templates.default = "plotly_dark"

# Chart 1: Bar Chart of Rankings
fig1 = px.bar(df.sort_values('Total Score', ascending=True), 
              x='Total Score', y='Central Bank', orientation='h',
              color='Total Score', color_continuous_scale='Viridis')
fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(size=24))
chart1_path = os.path.join(img_dir, 'chart1.png')
fig1.write_image(chart1_path, width=900, height=500)

# Chart 2: Spider/Radar for SNB vs BOJ
categories = ['Inflation Anchoring', 'Policy Consistency', 'Forecast Accuracy', 'Bond Confidence', 'FX Stability']
snb = df[df['Central Bank']=='SNB'].iloc[0, 1:6].values.tolist()
boj = df[df['Central Bank']=='BOJ'].iloc[0, 1:6].values.tolist()

fig2 = go.Figure()
fig2.add_trace(go.Scatterpolar(r=snb, theta=categories, fill='toself', name='SNB (Gold Standard)', line_color='#10B981'))
fig2.add_trace(go.Scatterpolar(r=boj, theta=categories, fill='toself', name='BOJ (Laggard)', line_color='#EF4444'))
fig2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 30])), showlegend=True, paper_bgcolor='rgba(0,0,0,0)', font=dict(size=20))
chart2_path = os.path.join(img_dir, 'chart2.png')
fig2.write_image(chart2_path, width=900, height=600)

# Generate PDF
pdf_path = os.path.join(out_dir, 'Premium_Data_Carousel.pdf')
c = canvas.Canvas(pdf_path, pagesize=(1080, 1350))

def bg():
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, 1080, 1350, fill=1, stroke=0)

# Slide 1
bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 40)
c.drawString(80, 1150, "THE DATA-DRIVEN TRUTH")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 100)
c.drawString(80, 1000, "Global Central Bank")
c.drawString(80, 880, "Credibility Index")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 40)
c.drawString(80, 750, "Rigorous 2020-2024 Macroeconomic Analysis")
c.showPage()

# Slide 2
bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 40)
c.drawString(80, 1200, "01 / GLOBAL LEADERBOARD")
c.drawImage(chart1_path, 80, 400, 920, 600, mask='auto')
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 50)
c.drawString(80, 300, "SNB & FED lead the pack.")
c.setFont(f_reg, 36)
c.setFillColor(TEXT_SEC)
c.drawString(80, 240, "Switzerland and the US maintained highest policy consistency.")
c.showPage()

# Slide 3
bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 40)
c.drawString(80, 1200, "02 / PILLAR BREAKDOWN: SNB vs BOJ")
c.drawImage(chart2_path, 80, 450, 920, 650, mask='auto')
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 50)
c.drawString(80, 350, "Why BOJ Fell Behind")
c.setFont(f_reg, 36)
c.setFillColor(TEXT_SEC)
c.drawString(80, 280, "While SNB maintained extreme FX stability and tight inflation")
c.drawString(80, 220, "anchoring, BOJ was penalized heavily for extreme FX volatility")
c.drawString(80, 160, "and the breakdown of Yield Curve Control (YCC).")
c.showPage()

c.save()
print('Premium Carousel Generated!')
