import os, json, requests
from datetime import datetime

# --- Configuration ---
DATA_FOLDER = "data"
BASE_URL = "https://almog787.github.io/sports-highlights-hub"
TSDB_API_URL = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t="

def ensure_env():
    if not os.path.exists(DATA_FOLDER): os.makedirs(DATA_FOLDER)
    # SEO Files
    with open("robots.txt", "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml")

def get_team_assets(team_name):
    """מושך לוגו מ-TheSportsDB"""
    try:
        url = f"{TSDB_API_URL}{requests.utils.quote(team_name)}"
        r = requests.get(url, timeout=5).json()
        if r.get('teams'):
            return r['teams'][0].get('strTeamBadge')
    except: pass
    return "https://www.thesportsdb.com/images/media/team/badge/small/default.png"

def fetch_data():
    ensure_env()
    print("Fetching highlights from ScoreBat...")
    try:
        sb_data = requests.get("https://www.scorebat.com/video-api/v3/").json().get('response', [])
    except: sb_data = []

    # Live Scores from API-Football
    live_scores = []
    api_key = os.environ.get("LIVE_API_KEY")
    if api_key:
        print("Fetching live scores from API-Football...")
        headers = {'x-apisports-key': api_key}
        try:
            r = requests.get("https://v3.football.api-sports.io/fixtures?live=all", headers=headers)
            live_scores = r.json().get('response', [])
        except: pass

    enriched_highlights = []
    categories = set()

    # Processing top 15 highlights for performance
    for item in sb_data[:15]:
        title = item.get("title", "")
        comp = item.get("competition", "International")
        categories.add(comp)
        
        # Split teams
        teams = title.split(' - ')
        home_team = teams[0] if len(teams) > 0 else "Home"
        away_team = teams[1] if len(teams) > 1 else "Away"

        enriched_highlights.append({
            "title": title,
            "competition": comp,
            "date": item.get("date"),
            "embed_code": item.get("videos", [{}])[0].get("embed"),
            "url": item.get("matchviewUrl"),
            "home_team": {"name": home_team, "logo": get_team_assets(home_team)},
            "away_team": {"name": away_team, "logo": get_team_assets(away_team)}
        })

    # Save all
    with open(f"{DATA_FOLDER}/sports_highlights.json", "w", encoding="utf-8") as f:
        json.dump(enriched_highlights, f, ensure_ascii=False, indent=4)
    with open(f"{DATA_FOLDER}/categories.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(categories)), f, ensure_ascii=False)
    with open(f"{DATA_FOLDER}/live_scores.json", "w", encoding="utf-8") as f:
        json.dump(live_scores, f, ensure_ascii=False)

    # Sitemap
    xml = ['<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml.append(f'<url><loc>{BASE_URL}/</loc><priority>1.0</priority></url>')
    for c in categories:
        xml.append(f'<url><loc>{BASE_URL}/?league={requests.utils.quote(c)}</loc></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w") as f: f.write("\n".join(xml))

if __name__ == "__main__":
    fetch_data()
