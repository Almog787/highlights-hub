import json
import os
from datetime import datetime

# --- Configuration ---
HIGHLIGHTS_FILE = "data/sports_highlights.json"
LIVE_SCORES_FILE = "data/live_scores.json"
README_FILE = "README.md"

# Updated Website URL
BASE_WEBSITE_URL = "https://almog787.github.io/sports-highlights-hub/"

def generate_readme():
    print(f"Updating README.md for: {BASE_WEBSITE_URL}")
    
    # Fail-safe: Check if data files exist
    if not os.path.exists(HIGHLIGHTS_FILE):
        print("Data file not found. Skipping README update.")
        return

    try:
        with open(HIGHLIGHTS_FILE, 'r', encoding='utf-8') as f:
            highlights = json.load(f)
        
        # Try to load live scores, default to empty list if fails
        live_scores = []
        if os.path.exists(LIVE_SCORES_FILE):
            with open(LIVE_SCORES_FILE, 'r', encoding='utf-8') as f:
                live_scores = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Content Building - Bilingual Header
    content = [
        "# 🏆 Sports Plus - Highlights & Live Scores Hub",
        "## ספורט פלוס - פורטל תקצירים ותוצאות בזמן אמת",
        f"\n> **Last Updated / עדכון אחרון:** {now}",
        "\n---",
        "\n### 📊 System Stats / סטטיסטיקות מערכת",
        f"- 📺 **Highlights available / תקצירים זמינים:** {len(highlights)}",
        f"- ⚽ **Current Live Matches / משחקים חיים כרגע:** {len(live_scores)}",
        "\n---",
        "\n### 🎬 Latest Highlights / תקצירים אחרונים",
        "| Match / משחק | League / ליגה | Date / תאריך |",
        "| :--- | :--- | :--- |"
    ]

    # Add last 7 highlights to the table
    for item in highlights[:7]:
        date_str = item.get('date', '')[:10]
        content.append(f"| {item['title']} | {item['competition']} | {date_str} |")

    content.append("\n---")
    
    # Project Description - English
    content.append("\n### 🚀 About the Project")
    content.append(f"This project is an automated sports aggregator. The live site is hosted here: [{BASE_WEBSITE_URL}]({BASE_WEBSITE_URL})")
    content.append("- **Automated Data Fetching:** Scrapes highlights and live scores every 30 minutes via GitHub Actions.")
    content.append("- **SEO Optimized:** Dynamic sitemap generation and static meta-data for search engines.")
    content.append("- **Bilingual Support:** Full support for Hebrew and English users.")
    
    # Project Description - Hebrew
    content.append("\n### 🚀 אודות הפרויקט")
    content.append(f"אגרגטור ספורט אוטומטי המבוסס על Python. האתר זמין בכתובת: [{BASE_WEBSITE_URL}]({BASE_WEBSITE_URL})")
    content.append("- **איסוף נתונים אוטומטי:** סריקת תקצירים ותוצאות חיות כל 30 דקות בעזרת GitHub Actions.")
    content.append("- **אופטימיזציית SEO:** יצירת מפת אתר דינמית (Sitemap) וניווט מבוסס URL.")
    content.append("- **תמיכה דו-לשונית:** ממשק מלא בעברית ובאנגלית.")

    content.append("\n---")
    content.append(f"\n## [🔗 Visit Live Site / כניסה לאתר החי]({BASE_WEBSITE_URL})")

    # Write to file
    try:
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        print("Bilingual README.md updated successfully with new URL.")
    except Exception as e:
        print(f"Error writing README: {e}")

if __name__ == "__main__":
    generate_readme()
