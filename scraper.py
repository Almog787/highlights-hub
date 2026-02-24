import json
import yt_dlp

def scrape_kindergarten():
    all_results = {}
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}

    # קטגוריות לחיפוש
    categories = {
        "holiday": "שירי פורים לילדים מחרוזת 2024",
        "movement": "שירי הפעלה ותנועה לילדים קטנים",
        "morning": "שירי בוקר טוב וריכוז לגן",
        "sleep": "מוזיקה רגועה לשינה לתינוקות ופעוטות"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for key, query in categories.items():
            print(f"🔍 אוסף תוכן עבור: {query}")
            category_items = []
            try:
                # מחפש את 15 התוצאות הכי רלוונטיות לכל קטגוריה
                info = ydl.extract_info(f"ytsearch15:{query}", download=False)
                for entry in info.get('entries', []):
                    if entry:
                        category_items.append({
                            "id": entry['id'],
                            "title": entry.get('title'),
                            "url": f"https://www.youtube.com/embed/{entry['id']}"
                        })
                all_results[key] = category_items
            except Exception as e:
                print(f"Error scraping {key}: {e}")

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print("✨ הדשבורד עודכן בהצלחה!")

if __name__ == "__main__":
    scrape_kindergarten()
