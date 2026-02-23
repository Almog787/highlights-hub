import json
import yt_dlp

def scrape_live_streams():
    # הגדרת קטגוריות וחיפושים
    queries = {
        "news": "live news stream world",
        "cartoons": "live cartoons for kids 24/7",
        "movies": "live movies stream full"
    }

    results = {}

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for category, query in queries.items():
            print(f"Searching for {category}...")
            # מחפש סרטונים שהם 'live' בלבד
            search_url = f"ytsearch10:{query} live" 
            try:
                info = ydl.extract_info(search_url, download=False)
                category_streams = []
                
                for entry in info['entries']:
                    if entry:
                        category_streams.append({
                            "id": entry['id'],
                            "title": entry['title'],
                            "url": f"https://www.youtube.com/embed/{entry['id']}",
                            "thumbnail": entry.get('thumbnail')
                        })
                results[category] = category_streams
            except Exception as e:
                print(f"Error scraping {category}: {e}")

    # שמירה לקובץ JSON
    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("Successfully updated streams.json")

if __name__ == "__main__":
    scrape_live_streams()
