import json
import yt_dlp
import re

def get_episode_number(title):
    match = re.search(r'פרק\s+(\d+)', title)
    return int(match.group(1)) if match else 999

def scrape_all():
    all_results = {}
    ydl_opts = {'quiet': True, 'extract_flat': True, 'skip_download': True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # --- 1. המומינים (Hebrew) ---
        print("🔍 Scraping The Moomins...")
        moomin_episodes = []
        info = ydl.extract_info("ytsearch40:המומינים פרק מלא", download=False)
        for entry in info.get('entries', []):
            if entry and 'המומינים' in entry.get('title', ''):
                moomin_episodes.append({
                    "id": entry['id'], "title": entry.get('title'),
                    "ep_num": get_episode_number(entry.get('title')),
                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                })
        moomin_episodes.sort(key=lambda x: x['ep_num'])
        all_results["moomins"] = moomin_episodes

        # --- 2. שירי פורים (Purim Songs) ---
        print("🔍 Scraping Purim Songs...")
        purim_songs = []
        info = ydl.extract_info("ytsearch20:שירי פורים לילדים מחרוזת", download=False)
        for entry in info.get('entries', []):
            if entry:
                purim_songs.append({
                    "id": entry['id'], "title": entry.get('title'),
                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                })
        all_results["purim"] = purim_songs

        # --- 3. שירי ילדים ישראלים (Israeli Kids Songs) ---
        print("🔍 Scraping Israeli Kids Songs...")
        kids_songs = []
        info = ydl.extract_info("ytsearch20:שירי ילדים ישראלים קלאסיים מחרוזת", download=False)
        for entry in info.get('entries', []):
            if entry:
                kids_songs.append({
                    "id": entry['id'], "title": entry.get('title'),
                    "url": f"https://www.youtube.com/embed/{entry['id']}"
                })
        all_results["kids_songs"] = kids_songs

        # --- 4. שידורי מצויירים חיים (Live) ---
        print("🔍 Scraping Live Cartoons...")
        live_streams = []
        live_queries = ["cartoon network live", "disney junior live"]
        for q in live_queries:
            info = ydl.extract_info(f"ytsearch5:{q} live", download=False)
            for entry in info.get('entries', []):
                if entry:
                    live_streams.append({
                        "id": entry['id'], "title": entry.get('title'),
                        "url": f"https://www.youtube.com/embed/{entry['id']}"
                    })
        all_results["cartoons"] = live_streams

    with open('streams.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    print("✨ Scrape Complete!")

if __name__ == "__main__":
    scrape_all()
