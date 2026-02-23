import os
import json
import requests
from datetime import datetime

# --- Configuration ---
DATA_FOLDER = "data"
HIGHLIGHTS_FILE = os.path.join(DATA_FOLDER, "sports_highlights.json")
CATEGORIES_FILE = os.path.join(DATA_FOLDER, "categories.json")
LIVE_SCORES_FILE = os.path.join(DATA_FOLDER, "live_scores.json")
SITEMAP_FILE = "sitemap.xml"

SCOREBAT_API_URL = "https://www.scorebat.com/video-api/v3/"
# Assuming usage of API-Football via RapidAPI or similar for live scores
LIVE_SCORES_API_URL = "https://v3.football.api-sports.io/fixtures?live=all"
LIVE_SCORES_API_KEY = os.environ.get("LIVE_API_KEY", "")

# Replace with your actual GitHub Pages URL later
BASE_WEBSITE_URL = "https://yourusername.github.io/your-repo-name"

def ensure_environment():
    """
    Fail-safe: Ensures all necessary directories and files exist.
    """
    try:
        if not os.path.exists(DATA_FOLDER):
            print(f"Creating directory: {DATA_FOLDER}")
            os.makedirs(DATA_FOLDER)
        
        for file_path in [HIGHLIGHTS_FILE, CATEGORIES_FILE, LIVE_SCORES_FILE]:
            if not os.path.exists(file_path):
                print(f"Creating initial file: {file_path}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
    except Exception as e:
        print(f"Critical error during environment setup: {e}")
        exit(1)

def fetch_highlights():
    """
    Fetches the latest highlights from ScoreBat.
    """
    print("Fetching highlights data...")
    try:
        response = requests.get(SCOREBAT_API_URL, timeout=15)
        response.raise_for_status()
        return response.json().get('response', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return []

def fetch_live_scores():
    """
    Fetches live scores if API key is present. Fail-safe returns empty if fails.
    """
    if not LIVE_SCORES_API_KEY:
        print("No LIVE_API_KEY found in environment. Skipping live scores fetch.")
        return []

    print("Fetching live scores...")
    headers = {
        'x-apisports-key': LIVE_SCORES_API_KEY
    }
    try:
        response = requests.get(LIVE_SCORES_API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get('response', [])
    except Exception as e:
        print(f"Error fetching live scores: {e}")
        return []

def generate_sitemap(categories):
    """
    Generates a dynamic sitemap.xml for SEO based on extracted categories.
    """
    print("Generating sitemap.xml...")
    try:
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        # Add main page
        xml_content.append(f'  <url>\n    <loc>{BASE_WEBSITE_URL}/</loc>\n    <changefreq>hourly</changefreq>\n  </url>')
        
        # Add dynamic category pages
        for category in categories:
            encoded_category = requests.utils.quote(category)
            url = f"{BASE_WEBSITE_URL}/?league={encoded_category}"
            xml_content.append(f'  <url>\n    <loc>{url}</loc>\n    <changefreq>hourly</changefreq>\n  </url>')
            
        xml_content.append('</urlset>')
        
        with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(xml_content))
        print("Sitemap generated successfully.")
    except Exception as e:
        print(f"Error generating sitemap: {e}")

def process_and_save_data(raw_highlights, raw_live_scores):
    """
    Processes all raw data, extracts categories, and saves everything.
    """
    processed_highlights = []
    unique_categories = set()

    for item in raw_highlights:
        competition = item.get("competition", "General")
        unique_categories.add(competition)
        
        clean_item = {
            "title": item.get("title"),
            "competition": competition,
            "thumbnail": item.get("thumbnail"),
            "embed_code": item.get("videos", [{}])[0].get("embed"),
            "date": item.get("date"),
            "timestamp": datetime.now().isoformat()
        }
        processed_highlights.append(clean_item)

    categories_list = sorted(list(unique_categories))

    try:
        with open(HIGHLIGHTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(processed_highlights, f, indent=4, ensure_ascii=False)
            
        with open(CATEGORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(categories_list, f, indent=4, ensure_ascii=False)
            
        with open(LIVE_SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump(raw_live_scores, f, indent=4, ensure_ascii=False)
            
        print(f"Saved {len(processed_highlights)} highlights, {len(categories_list)} categories, and {len(raw_live_scores)} live scores.")
        
        # Trigger sitemap generation based on categories
        generate_sitemap(categories_list)

    except Exception as e:
        print(f"Error saving processed data: {e}")

def main():
    print("--- Advanced Sports Aggregator Started ---")
    ensure_environment()
    
    highlights_data = fetch_highlights()
    live_scores_data = fetch_live_scores()
    
    process_and_save_data(highlights_data, live_scores_data)
    print("--- Process Completed ---")

if __name__ == "__main__":
    main()
