# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata
# app/models.py
from datetime import datetime, timezone

url_map = {}            # short_code -> original_url
reverse_url_map = {}    # original_url -> short_code
click_count = {}        # short_code -> int
url_metadata = {}       # short_code -> metadata dict

def save_url_mapping(original_url, short_code):
    url_map[short_code] = original_url
    reverse_url_map[original_url] = short_code
    click_count[short_code] = 0
    url_metadata[short_code] = {
        'created_at': datetime.now(timezone.utc).isoformat()
    }

def get_original_url(short_code):
    return url_map.get(short_code)

def increment_click(short_code):
    if short_code in click_count:
        click_count[short_code] += 1

def get_clicks(short_code):
    return click_count.get(short_code, 0)

def get_metadata(short_code):
    return url_metadata.get(short_code, {})
