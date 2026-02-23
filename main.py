import os
import json
import requests

DATA_FOLDER = "data"

def get_fallback_logo(team_name):
    """יוצר לוגו חלופי מעוצב אם אין לוגו מה-API"""
    bg_colors = ["0D6EFD", "DC3545", "198754", "6610F2", "FD7E14"]
    import hashlib
    # בחירת צבע קבוע לפי שם הקבוצה
    color_idx = int(hashlib.mdigest(team_name.encode()).hexdigest(), 16) % len(bg_colors)
    return f"https://ui-avatars.com/api/?name={team_name}&background={bg_colors[color_idx]}&color=fff&size=200&bold=true&font-size=0.33"

def fetch_and_organize_data():
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    print("Fetching global football highlights...")
    try:
        response = requests.get("https://www.scorebat.com/video-api/v3/").json()
        raw_matches = response.get('response', [])
    except Exception as e:
        print(f"Error: {e}")
        raw_matches = []

    organized_data = {}

    for item in raw_matches[:40]: # לוקחים מספיק משחקים לחלוקה
        comp = item.get("competition", "International")
        title = item.get("title", "")
        teams = title.split(' - ')
        
        home_n = teams[0] if len(teams) > 0 else "Home"
        away_n = teams[1] if len(teams) > 1 else "Away"

        match_entry = {
            "title": title,
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

        if comp not in organized_data:
            organized_data[comp] = []
        organized_data[comp].append(match_entry)

    with open(f"{DATA_FOLDER}/highlights.json", "w", encoding="utf-8") as f:
        json.dump(organized_data, f, ensure_ascii=False, indent=4)
    print("Data organized by league and saved.")

if __name__ == "__main__":
    fetch_and_organize_data()
