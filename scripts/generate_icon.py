from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont
import os

# 以台北時區跑（Asia/Taipei = UTC+8）
tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
yyyy_mm_dd = now.strftime("%Y-%m-%d")
day_num = now.strftime("%d")           # 01–31
# weekday_cn = "日一二三四五六"[int(now.strftime("%w"))]  # 0=日
weekday_en = now.strftime("%a")

os.makedirs("images", exist_ok=True)
out_path = f"images/{yyyy_mm_dd}.png"

# 512x512 畫布
W, H = 512, 512
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 圓角白底卡片
card_radius = 64
draw.rounded_rectangle([0, 0, W, H], radius=card_radius, fill=(255, 255, 255, 255))

# 上方紅色條
header_h = 160
draw.rounded_rectangle([0, 0, W, header_h], radius=card_radius, fill=(229, 57, 53, 255))
draw.rectangle([0, card_radius, W, header_h], fill=(229, 57, 53, 255))  # 抹平上圓角

# 載入字型（GitHub Actions 內建 DejaVu）
def load_font(name, size):
    try:
        return ImageFont.truetype(name, size=size)
    except:
        return ImageFont.load_default()

font_month = load_font("DejaVuSans-Bold.ttf", 72)
font_day   = load_font("DejaVuSans-Bold.ttf", 220)
font_wd    = load_font("DejaVuSans.ttf", 56)

# Header 顯示「AUG 2025」或「2025-08」
month_text = now.strftime("%b %Y").upper()  # e.g., AUG 2025
w, h = draw.textbbox((0,0), month_text, font=font_month)[2:]
draw.text(((W - w) / 2, (header_h - h) / 2), month_text, font=font_month, fill=(255,255,255,255))

# 下方日期（大字）
day_text = str(int(day_num))  # 去掉前導 0
w, h = draw.textbbox((0,0), day_text, font=font_day)[2:]
draw.text(((W - w) / 2, header_h + (H - header_h - h) / 2 - 20), day_text, font=font_day, fill=(66,66,66,255))

# 右下角星期
# wd_text = f"週{weekday_cn}"
wd_text = weekday_en

w, h = draw.textbbox((0,0), wd_text, font=font_wd)[2:]
margin = 24
draw.text((W - w - margin, H - h - margin), wd_text, font=font_wd, fill=(120,120,120,255))

img.save(out_path, "PNG")
print(out_path)
