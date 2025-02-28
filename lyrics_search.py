import os
import requests
from dotenv import load_dotenv

load_dotenv()

class LyricsSearch:
    def __init__(self):
        self.base_url = "https://api.genius.com"
        self.headers = {
            'Authorization': f'Bearer {os.getenv("GENIUS_ACCESS_TOKEN")}'
        }

    def search_song(self, query):
        """Search for songs using lyrics or song title."""
        search_url = f"{self.base_url}/search"
        params = {'q': query}

        try:
            response = requests.get(search_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            if 'response' not in data:
                return None

            hits = data['response']['hits']
            if not hits:
                return None

            results = []
            for hit in hits[:5]:  # Get top 5 results
                song = hit['result']
                results.append({
                    'title': song['title'],
                    'artist': song['primary_artist']['name'],
                    'url': song['url'],
                    'thumbnail': song['song_art_image_thumbnail_url']
                })

            return results

        except Exception as e:
            print(f"Error in lyrics search: {str(e)}")
            return None

    def get_lyrics_preview(self, url):
        """Get a preview of the lyrics from the song's page."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Note: This is a simplified version. In a production environment,
            # you would want to properly parse the HTML and extract the lyrics.
            return "Lyrics preview unavailable. Click the link to view full lyrics."
        except Exception as e:
            print(f"Error getting lyrics: {str(e)}")
            return None
