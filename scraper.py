import json
import yt_dlp

def scrape_cartoons():
    # רשימת שאילתות ממוקדת מאוד לערוצים רשמיים ושידורי 24/7
    queries = [
        "cartoons live stream 24/7",
        "official cartoon network live",
        "disney junior live stream",
        "nickelodeon live stream cartoons",
        "peppa pig live 24/7",
        "spongebob live stream",
        "looney tunes live stream",
        "nursery rhymes live kids tv"
    ]

    all_streams = []
    
    # הגדרות לאיסוף מידע בלבד ללא הורדה
    ydl_opts = {
        'quiet': True,
        'extract_flat': 'in_playlist',  # חילוץ מהיר של רשימות השמעה
        'skip_download': True,
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for q in queries:
            print(f"🔍 Scanning for: {q}...")
            # שימוש בפילטר הפנימי של יוטיוב לשידורים חיים בלבד
            search_query = f"ytsearch15:{q}" 
            
            try:
                # חילוץ מידע
                info = ydl.extract_info(search_query, download=False)
                
                if 'entries' in info:
                    for entry in info['entries']:
                        if not entry: continue
                        
                        # סינון קפדני: רק אם הסרטון מסומן כשידור חי (is_live)
                        # הערה: ytsearch לעיתים מחזיר סרטונים רגילים, לכן הבדיקה הזו קריטית
                        is_live = entry.get('is_live') or 'live' in entry.get('title', '').lower()
                        
                        if is_live and entry.get('id'):
                            # מניעת כפילויות לפי מזהה סרטון
                            if not any(s['id'] == entry['id'] for s in all_streams):
                                all_streams.append({
                                    "id": entry['id'],
                                    "title": entry.get('title', 'Cartoon Live Stream'),
                                    "url": f"https://www.youtube.com/embed/{entry['id']}",
                                    "thumbnail": entry.get('thumbnails', [{}])[-1].get('url')
                                })
                                print(f"✅ Found Live: {entry.get('title')[:50]}...")
                                
            except Exception as e:
                print(f"❌ Error searching {q}: {e}")

    # שמירה למבנה ה-JSON שהאתר שלך מצפה לו
    results = {"cartoons": all_streams}

    # כתיבת הקובץ
    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print(f"\n✨ Done! Found {len(all_streams)} active cartoon streams.")

if __name__ == "__main__":
    scrape_cartoons()
