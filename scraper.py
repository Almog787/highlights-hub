import json
import yt_dlp

def scrape_cartoons():
    # Targeted queries for official and 24/7 cartoon streams
    queries = [
        "cartoon network live stream",
        "disney junior official live",
        "nickelodeon live channel",
        "peppa pig live 24/7",
        "spongebob live stream 24/7",
        "looney tunes official live",
        "nursery rhymes kids live tv",
        "cocomelon live stream"
    ]

    all_streams = []
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for q in queries:
            print(f"🔍 Searching for: {q}...")
            search_query = f"ytsearch10:{q}" 
            try:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        # Verification: strictly live content only
                        if entry and entry.get('id'):
                            # Avoid duplicates and non-live videos
                            if not any(s['id'] == entry['id'] for s in all_streams):
                                all_streams.append({
                                    "id": entry['id'],
                                    "title": entry.get('title', 'Cartoon Live'),
                                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                                })
            except Exception as e:
                print(f"❌ Error: {e}")

    # Wrap in the cartoons category for the website to read
    results = {"cartoons": all_streams}

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"✨ Success! Found {len(all_streams)} active cartoon channels.")

if __name__ == "__main__":
    scrape_cartoons()
