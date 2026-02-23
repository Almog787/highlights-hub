import os
import json
import requests
import hashlib

DATA_FOLDER = "data"

def get_fallback_logo(team_name):
    """יוצר לוגו חלופי מעוצב עם צבע קבוע לכל קבוצה"""
    bg_colors = ["0D6EFD", "DC3545", "198754", "6610F2", "FD7E14", "000000"]
    
    # יצירת מזהה ייחודי (Hash) משם הקבוצה כדי שהצבע יישאר קבוע
    team_hash = hashlib.md5(team_name.encode()).hexdigest()
    color_idx = int(team_hash, 16) % len(bg_colors)
    
    # ניקוי שם הקבוצה לטובת ה-URL (הסרת רווחים ותווים מיוחדים)
    safe_name = requests.utils.quote(team_name)
    
    return f"https://ui-avatars.com/api/?name={safe_name}&background={bg_colors[color_idx]}&color=fff&size=200&bold=true&font-size=0.33"

def fetch_and_organize_data():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    print("Fetching global football highlights...")
    try:
        # שליפת נתונים מ-ScoreBat
        response = requests.get("https://www.scorebat.com/video-api/v3/").json()
        raw_matches = response.get('response', [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        raw_matches = []

    organized_data = {}

    for item in raw_matches[:40]:
        comp = item.get("competition", "International")
        title = item.get("title", "")
        
        # הפרדת שמות הקבוצות מהכותרת
        if " - " in title:
            teams = title.split(' - ')
            home_n = teams[0].strip()
            away_n = teams[1].strip()
        else:
            home_n = title
            away_n = "Opponent"

        match_entry = {
            "title": title,
            "competition": comp,
            "date": item.get("date"),
            "embed_code": item.get("videos", [{}])[0].get("embed"),
            "url": item.get("matchviewUrl"),
            "home_team": {
                "name": home_n,
                "logo": get_fallback_logo(home_n)
            },
            "away_team": {
                "name": away_n,
                "logo": get_fallback_logo(away_n)
            }
        }

        # ארגון לפי ליגות
        if comp not in organized_data:
            organized_data[comp] = []
        organized_data[comp].append(match_entry)

    # שמירה לקובץ JSON
    with open(f"{DATA_FOLDER}/highlights.json", "w", encoding="utf-8") as f:
        json.dump(organized_data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully saved {len(raw_matches)} matches organized by league.")

if __name__ == "__main__":
    fetch_and_organize_data()
