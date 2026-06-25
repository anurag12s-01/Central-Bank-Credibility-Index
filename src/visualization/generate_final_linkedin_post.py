import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
out_dir = os.path.join(base_dir, 'docs')
img_dir = os.path.join(base_dir, 'docs', 'temp_images')
os.makedirs(out_dir, exist_ok=True)

try:
    pdfmetrics.registerFont(TTFont('Inter', 'C:\\Windows\\Fonts\\arial.ttf'))
    pdfmetrics.registerFont(TTFont('Inter-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
    f_reg, f_bold = 'Inter', 'Inter-Bold'
except:
    f_reg, f_bold = 'Helvetica', 'Helvetica-Bold'

BG_COLOR = HexColor('#0B0F19')
TEXT_PRI = HexColor('#F8FAFC')
TEXT_SEC = HexColor('#94A3B8')
ACCENT_BLU = HexColor('#3B82F6')
ACCENT_GRN = HexColor('#10B981')
ACCENT_PUR = HexColor('#8B5CF6')
ACCENT_RED = HexColor('#EF4444')

chart1_path = os.path.join(img_dir, 'chart1.png')

pdf_path = os.path.join(out_dir, 'CBCI_LinkedIn_Final.pdf')
c = canvas.Canvas(pdf_path, pagesize=(1080, 1350))

def draw_bg():
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, 1080, 1350, fill=1, stroke=0)

# Slide 1: Intro
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1150, "QUANTITATIVE MACRO PROJECT")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 110)
c.drawString(80, 980, "The Central Bank")
c.drawString(80, 860, "Credibility Index")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 42)
c.drawString(80, 720, "A data-driven approach to measuring trust,")
c.drawString(80, 660, "consistency, and efficacy in monetary policy.")
c.showPage()

# Slide 2: Motive
draw_bg()
c.setFillColor(ACCENT_PUR)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "01 / PROJECT MOTIVE")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Why Build This Index?")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 40)
text2 = [
    "The 2022 inflation shock proved that we cannot",
    "simply rely on central bank rhetoric. Market trust",
    "is fragile.",
    "",
    "I wanted to build a rigorous, quantitative framework",
    "that grades the world's top 10 central banks not",
    "on what they say, but on the mathematical reality",
    "of their macroeconomic execution over the last",
    "four volatile years (2020-2024)."
]
y_p = 850
for line in text2:
    c.drawString(80, y_p, line)
    y_p -= 55
c.showPage()

# Slide 3: Analysis
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "02 / THE ANALYSIS FRAMEWORK")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "How is it Calculated?")

pillars = [
    ("Inflation Anchoring (30%)", "Deviation from the 2.0% CPI target."),
    ("Policy Consistency (20%)", "FinBERT AI sentiment of press releases."),
    ("Forecast Accuracy (20%)", "Historical projections vs realized GDP/CPI."),
    ("Bond Confidence (15%)", "Sovereign yield curve volatility."),
    ("FX Stability (15%)", "Currency exchange stability via FRED API.")
]
y_pos = 850
for title, desc in pillars:
    c.setFillColor(HexColor('#1E293B'))
    c.roundRect(80, y_pos - 80, 920, 110, 20, fill=1, stroke=0)
    c.setFillColor(TEXT_PRI)
    c.setFont(f_bold, 36)
    c.drawString(120, y_pos - 25, title)
    c.setFillColor(ACCENT_GRN)
    c.setFont(f_reg, 28)
    c.drawString(120, y_pos - 65, desc)
    y_pos -= 130
c.showPage()

# Slide 4: Outcome
draw_bg()
c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "03 / THE OUTCOME")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "The Global Leaderboard")

if os.path.exists(chart1_path):
    c.drawImage(chart1_path, 80, 450, 920, 500, mask='auto')

c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 40)
c.drawString(80, 350, "Insight: SNB & FED Lead the Pack")
c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 32)
c.drawString(80, 290, "Switzerland and the US navigated the shock with the highest")
c.drawString(80, 240, "overall credibility, while the BOJ was penalized heavily for")
c.drawString(80, 190, "extreme FX volatility and YCC breakdown.")
c.showPage()

# Slide 5: Precautions
draw_bg()
c.setFillColor(ACCENT_RED)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "04 / PRECAUTIONS & LIMITATIONS")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "Methodological Nuance")

c.setFillColor(HexColor('#3F1D1D'))
c.roundRect(80, 450, 920, 500, 20, fill=1, stroke=0)

text5 = [
    "⚠️ Proxy Data Reliance",
    "Certain metrics, like Forecast Accuracy, rely on",
    "proxy consensus approximations rather than",
    "full historical dot-plot scraping.",
    "",
    "🤖 NLP Context Limits",
    "The FinBERT engine analyzes localized",
    "sentiment but struggles to fully capture the",
    "multi-decade cultural nuance of banks like the PBOC.",
    "",
    "It is a framework, not absolute financial truth."
]

c.setFillColor(TEXT_PRI)
c.setFont(f_reg, 40)
y_p = 860
for line in text5:
    if line.startswith("⚠️") or line.startswith("🤖"):
        c.setFont(f_bold, 46)
        c.setFillColor(ACCENT_RED)
    elif line.startswith("It is"):
        c.setFont(f_bold, 40)
        c.setFillColor(TEXT_PRI)
    else:
        c.setFont(f_reg, 36)
        c.setFillColor(TEXT_SEC)
    c.drawString(140, y_p, line)
    y_p -= 50
c.showPage()

# Slide 6: Connect
draw_bg()
c.setFillColor(ACCENT_BLU)
c.setFont(f_bold, 36)
c.drawString(80, 1200, "05 / JOIN THE DISCUSSION")
c.setFillColor(TEXT_PRI)
c.setFont(f_bold, 80)
c.drawString(80, 1050, "What do you think?")

c.setFillColor(TEXT_SEC)
c.setFont(f_reg, 40)
c.drawString(80, 850, "Does the data match your experience trading")
c.drawString(80, 790, "these sovereign markets?")

c.setFillColor(ACCENT_GRN)
c.setFont(f_bold, 50)
c.drawString(80, 600, "Let's Connect & Discuss 👇")

c.setFillColor(TEXT_PRI)
c.setFont(f_reg, 36)
c.drawString(80, 500, "I am actively building quantitative macroeconomic")
c.drawString(80, 440, "models and would love to exchange ideas with")
c.drawString(80, 380, "fellow analysts and economists.")

c.setStrokeColor(HexColor('#334155'))
c.setLineWidth(2)
c.line(80, 300, 1000, 300)

c.setFont(f_reg, 30)
c.setFillColor(TEXT_SEC)
c.drawString(80, 240, "Follow for more Python-driven macro insights.")

c.showPage()
c.save()
print('Final LinkedIn Post Carousel Generated!')
