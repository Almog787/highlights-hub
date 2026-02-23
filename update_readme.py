import json
import os
from datetime import datetime

# --- Configuration ---
HIGHLIGHTS_FILE = "data/sports_highlights.json"
LIVE_SCORES_FILE = "data/live_scores.json"
README_FILE = "README.md"

def generate_readme():
    print("Updating README.md with bilingual content...")
    
    # Fail-safe: Check if data files exist
    if not os.path.exists(HIGHLIGHTS_FILE):
        print("Data file not found. Skipping README update.")
        return

    with open(HIGHLIGHTS_FILE, 'r', encoding='utf-8') as f:
        highlights = json.load(f)
    
    with open(LIVE_SCORES_FILE, 'r', encoding='utf-8') as f:
        live_scores = json.load(f)

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Content Building
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
        content.append(f"| {item['title']} | {item['competition']} | {item['date'][:10]} |")

    content.append("\n---")
    
    # Project Description - English
    content.append("\n### 🚀 About the Project")
    content.append("This project is an automated sports aggregator built with **Python** and **GitHub Actions**.")
    content.append("- **Automated Data Fetching:** Scrapes highlights and live scores every 30 minutes.")
    content.append("- **SEO Optimized:** Dynamic sitemap generation for better indexing.")
    content.append("- **Zero Hosting Costs:** Runs entirely on GitHub infrastructure.")
    
    # Project Description - Hebrew
    content.append("\n### 🚀 אודות הפרויקט")
    content.append("פרויקט זה הוא אגרגטור ספורט אוטומטי המבוסס על **Python** ו-**GitHub Actions**.")
    content.append("- **איסוף נתונים אוטומטי:** סריקת תקצירים ותוצאות חיות כל 30 דקות.")
    content.append("- **אופטימיזציית SEO:** יצירת מפת אתר דינמית לאינדוקס מקסימלי.")
    content.append("- **אפס עלויות שרת:** רץ לחלוטין על התשתית של GitHub.")

    content.append("\n---")
    content.append("\n## [🔗 Visit Live Site / כניסה לאתר החי](https://yourusername.github.io/your-repo-name/)")

    # Write to file
    try:
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        print("Bilingual README.md updated successfully.")
    except Exception as e:
        print(f"Error writing README: {e}")

if __name__ == "__main__":
    generate_readme()
    
