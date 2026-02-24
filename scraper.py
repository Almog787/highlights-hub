import json
import yt_dlp

def scrape_kindergarten_content():
    all_results = {}
    # שימוש ב-ydl_opts מהיר ללא הורדה
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}

    # הגדרת שאילתות חיפוש ממוקדות לגננות - ללא "המומינים"
    categories = {
        "purim": "שירי פורים לילדים מחרוזת 2024",
        "morning": "שירי בוקר טוב למפגש בגן ילדים",
        "movement": "שירי הפעלה ותנועה לילדים מירב האוסמן אריאלה סביר",
        "classics": "שירי ילדות ישראלית קלאסיים לילדים",
        "relax": "מוזיקה רגועה למנוחה בגן ילדים"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for key, query in categories.items():
            print(f"🔄 סורק תוכן עבור: {query}")
            category_list = []
            try:
                # איסוף 12 סרטונים מכל קטגוריה
                results = ydl.extract_info(f"ytsearch12:{query}", download=False)
                if 'entries' in results:
                    for entry in results['entries']:
                        if entry:
                            category_list.append({
                                "id": entry['id'],
                                "title": entry.get('title').split('|')[0].split('(')[0].strip(), # ניקוי כותרות
                                "url": f"https://www.youtube.com/embed/{entry['id']}?rel=0"
                            })
                all_results[key] = category_list
            except Exception as e:
                print(f"שגיאה באיסוף {key}: {e}")

    # שמירה לקובץ ה-JSON שמזין את האתר
    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print("✨ הדשבורד עודכן בהצלחה ללא תוכניות טלוויזיה!")

if __name__ == "__main__":
    scrape_kindergarten_content()
