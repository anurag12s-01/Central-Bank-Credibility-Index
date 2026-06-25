import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd

# Try to register a modern font, fallback to Helvetica
try:
    pdfmetrics.registerFont(TTFont('Inter', 'C:\\Windows\\Fonts\\arial.ttf'))
    font_reg = 'Inter'
    pdfmetrics.registerFont(TTFont('Inter-Bold', 'C:\\Windows\\Fonts\\arialbd.ttf'))
    font_bold = 'Inter-Bold'
except:
    font_reg = 'Helvetica'
    font_bold = 'Helvetica-Bold'

# Slide Dimensions (LinkedIn Portrait: 1080x1350 px -> approx 15x18.75 inches at 72dpi)
# Let's use exactly 1080 x 1350 points for 1:1 pixel mapping
PAGE_WIDTH = 1080
PAGE_HEIGHT = 1350

# Colors
BG_COLOR = HexColor('#0B0F19') # Deep slate
TEXT_PRIMARY = HexColor('#F8FAFC')
TEXT_SECONDARY = HexColor('#94A3B8')
ACCENT_BLUE = HexColor('#3B82F6')
ACCENT_GREEN = HexColor('#10B981')
ACCENT_RED = HexColor('#EF4444')

# Load Data
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
df_scores = pd.read_csv(os.path.join(base_dir, 'data', 'processed', 'authentic_cbci_scores.csv'))

out_dir = os.path.join(base_dir, 'docs')
os.makedirs(out_dir, exist_ok=True)
pdf_path = os.path.join(out_dir, 'LinkedIn_Carousel_Final.pdf')

c = canvas.Canvas(pdf_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

def draw_bg(c):
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

# --- SLIDE 1: INTRO ---
draw_bg(c)
img1_path = r'C:\Users\anurag singh\.gemini\antigravity\brain\537a49af-9311-42f9-9c68-b8ba9f34615e\cover_illustration_1782425696961.png'
if os.path.exists(img1_path):
    c.drawImage(img1_path, 40, PAGE_HEIGHT - 650, PAGE_WIDTH - 80, 500, mask='auto')

c.setFillColor(ACCENT_BLUE)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 750, "QUANTITATIVE MACRO ANALYSIS")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 110)
c.drawString(80, PAGE_HEIGHT - 900, "The Central Bank")
c.drawString(80, PAGE_HEIGHT - 1020, "Credibility Index")

c.setFillColor(TEXT_SECONDARY)
c.setFont(font_reg, 42)
c.drawString(80, PAGE_HEIGHT - 1120, "Measuring trust, consistency, and efficacy")
c.drawString(80, PAGE_HEIGHT - 1180, "of global monetary policy in 2024.")
c.showPage()

# --- SLIDE 2: THE PROBLEM ---
draw_bg(c)
c.setFillColor(ACCENT_RED)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 120, "01 / THE PROBLEM")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 80)
c.drawString(80, PAGE_HEIGHT - 250, "The Global Inflation Shock")

c.setFillColor(TEXT_SECONDARY)
c.setFont(font_reg, 36)
c.drawString(80, PAGE_HEIGHT - 350, "Since 2022, central banks have battled the worst inflation shock in 40 years.")

img2_path = r'C:\Users\anurag singh\.gemini\antigravity\brain\537a49af-9311-42f9-9c68-b8ba9f34615e\shock_illustration_1782425713740.png'
if os.path.exists(img2_path):
    c.drawImage(img2_path, 40, 200, PAGE_WIDTH - 80, PAGE_HEIGHT - 650, mask='auto')
else:
    c.setStrokeColor(HexColor('#1E293B'))
    c.setLineWidth(4)
    c.rect(80, 200, PAGE_WIDTH - 160, PAGE_HEIGHT - 650, stroke=1, fill=0)

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 120)
c.drawString(120, 350, "4.98%")
c.setFont(font_reg, 32)
c.setFillColor(TEXT_SECONDARY)
c.drawString(120, 300, "Peak US 10-Year Treasury Yield (Oct 2023)")
c.showPage()

# --- SLIDE 3: THE FRAMEWORK ---
draw_bg(c)
c.setFillColor(ACCENT_BLUE)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 120, "02 / THE FRAMEWORK")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 80)
c.drawString(80, PAGE_HEIGHT - 250, "How We Measure Credibility")

img3_path = r'C:\Users\anurag singh\.gemini\antigravity\brain\537a49af-9311-42f9-9c68-b8ba9f34615e\ai_illustration_1782425729704.png'
if os.path.exists(img3_path):
    c.drawImage(img3_path, 40, PAGE_HEIGHT - 600, PAGE_WIDTH - 80, 400, mask='auto')

# Draw 5 blocks for the pillars
pillars = [
    ("Inflation Anchoring (30%)", "Actual CPI vs Target Rates"),
    ("Policy Consistency (20%)", "NLP FinBERT Sentiment Analysis"),
    ("Forecast Accuracy (20%)", "Historical Projections vs Reality"),
    ("Bond Confidence (15%)", "Sovereign Yield Volatility"),
    ("FX Stability (15%)", "FRED Currency Exchange Metrics")
]

y_pos = PAGE_HEIGHT - 620
for title, desc in pillars:
    c.setFillColor(HexColor('#1E293B'))
    c.roundRect(80, y_pos - 80, PAGE_WIDTH - 160, 100, 20, fill=1, stroke=0)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont(font_bold, 34)
    c.drawString(120, y_pos - 30, title)
    
    c.setFillColor(ACCENT_GREEN)
    c.setFont(font_reg, 26)
    c.drawString(120, y_pos - 65, desc)
    y_pos -= 120

c.showPage()

# --- SLIDE 4: THE ANALYSIS ---
draw_bg(c)
c.setFillColor(ACCENT_GREEN)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 120, "03 / THE ANALYSIS")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 80)
c.drawString(80, PAGE_HEIGHT - 250, "Global Leaderboard")

# Draw the table
y_pos = PAGE_HEIGHT - 380
for i, row in df_scores.head(10).iterrows():
    bank = row['Central Bank']
    score = row['Total Score']
    
    c.setFillColor(HexColor('#1E293B'))
    c.roundRect(80, y_pos - 60, PAGE_WIDTH - 160, 80, 10, fill=1, stroke=0)
    
    c.setFillColor(TEXT_PRIMARY)
    c.setFont(font_bold, 40)
    c.drawString(120, y_pos - 40, f"#{i+1}  {bank}")
    
    c.setFillColor(ACCENT_BLUE if score > 80 else ACCENT_RED)
    c.drawRightString(PAGE_WIDTH - 120, y_pos - 40, f"{score:.1f} pts")
    y_pos -= 90

c.showPage()

# --- SLIDE 5: THE OUTCOME ---
draw_bg(c)
c.setFillColor(ACCENT_GREEN)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 120, "04 / THE OUTCOME")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 80)
c.drawString(80, PAGE_HEIGHT - 250, "Winners & Laggards")

# Winners
c.setFillColor(HexColor('#064E3B'))
c.roundRect(80, PAGE_HEIGHT - 600, PAGE_WIDTH - 160, 300, 20, fill=1, stroke=0)
c.setFillColor(ACCENT_GREEN)
c.setFont(font_bold, 50)
c.drawString(120, PAGE_HEIGHT - 380, "🏆 THE WINNERS: SNB & FED")
c.setFillColor(TEXT_PRIMARY)
c.setFont(font_reg, 36)
c.drawString(120, PAGE_HEIGHT - 460, "Aggressive early rate hikes secured")
c.drawString(120, PAGE_HEIGHT - 520, "long-term bond market confidence.")

# Laggards
c.setFillColor(HexColor('#7F1D1D'))
c.roundRect(80, PAGE_HEIGHT - 1000, PAGE_WIDTH - 160, 300, 20, fill=1, stroke=0)
c.setFillColor(ACCENT_RED)
c.setFont(font_bold, 50)
c.drawString(120, PAGE_HEIGHT - 780, "⚠️ THE LAGGARDS: PBOC & RBI")
c.setFillColor(TEXT_PRIMARY)
c.setFont(font_reg, 36)
c.drawString(120, PAGE_HEIGHT - 860, "Structural constraints led to high FX")
c.drawString(120, PAGE_HEIGHT - 920, "volatility and lower inflation anchoring.")
c.showPage()

# --- SLIDE 6: STRATEGIC TAKEAWAY ---
draw_bg(c)
c.setFillColor(ACCENT_BLUE)
c.setFont(font_bold, 36)
c.drawString(80, PAGE_HEIGHT - 120, "05 / INVESTOR STRATEGY")

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_bold, 80)
c.drawString(80, PAGE_HEIGHT - 250, "Portfolio Positioning")

c.setFillColor(HexColor('#1E293B'))
c.roundRect(80, 200, PAGE_WIDTH - 160, PAGE_HEIGHT - 500, 20, fill=1, stroke=0)

text = [
    "1. Overweight Sovereign Bonds in Tier 1",
    "   jurisdictions (SNB, FED, ECB).",
    "",
    "2. Utilize AI NLP models to front-run",
    "   central bank policy pivots.",
    "",
    "3. Hedge FX exposure in lower-tier",
    "   credibility regimes to mitigate",
    "   unpriced tail risks."
]

c.setFillColor(TEXT_PRIMARY)
c.setFont(font_reg, 42)
y_p = PAGE_HEIGHT - 350
for line in text:
    c.drawString(140, y_p, line)
    y_p -= 60

c.showPage()
c.save()
print('Successfully generated LinkedIn Carousel PDF!')
