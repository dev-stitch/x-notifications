import json
import time
import gzip
from io import BytesIO
import requests
from datetime import datetime
from playwright.async_api import async_playwright
import asyncio
webhook_url = "" # webhook here
user = "janeremover" # target twitter/x here
class tweet_scraper:
    def __init__(self):
        self.existing_tweets = self.load_existing_tweets()
        self.last_check_time = time.time()
    def load_existing_tweets(self):
        try:
            with open('tweets.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'tweets': []}
    def save_tweets(self):
        with open('tweets.json', 'w') as f:
            json.dump(self.existing_tweets, f, indent=2)
    def send_to_discord(self, tweet_info):
        text = tweet_info.get('text', '')
        if not text or text == 'None':
            text = "[no text content]"
        if len(text) > 2000:
            text = text[:1997] + "..."
        embed = {
            "title": f"new tweet from @{user}",
            "description": text,
            "color": 3447003,
            "fields": [],
            "url": f"https://twitter.com/{user}/status/{tweet_info['id']}"
        }
        stats = [("likes", tweet_info.get('likes', 0)), ("retweets", tweet_info.get('retweets', 0)), ("views", tweet_info.get('views', 0))]
        for name, value in stats:
            if isinstance(value, (int, float)):
                embed["fields"].append({"name": name, "value": str(value), "inline": True})
        try:
            created_at = tweet_info.get('created_at')
            if created_at:
                if isinstance(created_at, str) and not created_at.endswith('Z'):
                    dt = datetime.strptime(created_at, '%a %b %d %H:%M:%S %z %Y')
                    embed["timestamp"] = dt.isoformat()
                else:
                    embed["timestamp"] = created_at
        except Exception as e:
            print(f"an error has occured! - {e}")
        if 'media' in tweet_info and tweet_info['media']:
            first_media = tweet_info['media'][0]
            media_url = first_media.get('media_url_https')
            if media_url:
                if first_media.get('type') == 'photo':
                    embed["image"] = {"url": media_url}
                else:
                    embed["fields"].append({"name": "media", "value": f"[media link]({media_url})", "inline": False})      
        payload = {
            "content": f"@everyone https://twitter.com/{user}/status/{tweet_info['id']}",
            "embeds": [embed],
            "username": "twitter notifications",
            "avatar_url": "https://abs.twimg.com/favicons/twitter.ico"
        }
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            print(f"sent tweet - {tweet_info['id']} - to discord")
            time.sleep(1)
        except requests.exceptions.HTTPError as e:
            print(f"an error has occured! - {e.response.status_code} - {e.response.text}")
        except Exception as e:
            print(f"an error has occured posting to discord -  {e}")
    def process_tweet(self, tweet_data):
        tweet_id = tweet_data['result']['rest_id']
        for tweet in self.existing_tweets['tweets']:
            if tweet['id'] == tweet_id:
                return False 
        tweet_info = {
            'id': tweet_id,
            'created_at': tweet_data['result']['legacy']['created_at'],
            'text': tweet_data.get('result', {}).get('legacy', {}).get('full_text', ''),
            'likes': tweet_data['result']['legacy'].get('favorite_count', 0),
            'retweets': tweet_data['result']['legacy'].get('retweet_count', 0),
            'views': tweet_data['result'].get('views', {}).get('count', 0)
        }
        if 'media' in tweet_data['result']['legacy'].get('entities', {}):
            tweet_info['media'] = tweet_data['result']['legacy']['entities']['media']
        self.existing_tweets['tweets'].append(tweet_info)
        self.send_to_discord(tweet_info)
        return True
    async def scrape_tweets(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            xhr_requests = []
            def request_handler(request):
                if request.resource_type == "xhr" and "UserTweets?variables" in request.url:
                    xhr_requests.append(request)
            page.on("request", request_handler)
            try:
                await page.goto(f'https://x.com/{user}', wait_until="networkidle")
                await asyncio.sleep(2)
                for _ in range(3):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    await asyncio.sleep(1)
                new_tweets_found = False
                for request in xhr_requests:
                    try:
                        response = await request.response()
                        if response:
                            try:
                                response_data = await response.json()
                                if not response_data:
                                    continue
                                timeline_entries = response_data['data']['user']['result']['timeline']['timeline'].get('instructions', [])
                                for instruction in timeline_entries:
                                    if instruction.get('type') in ['TimelinePinEntry', 'TimelineAddEntries']:
                                        entries = [instruction['entry']] if 'entry' in instruction else instruction.get('entries', [])
                                        for entry in entries:
                                            if 'content' in entry and 'itemContent' in entry['content']:
                                                tweet_data = entry['content']['itemContent'].get('tweet_results', {})
                                                if tweet_data and self.process_tweet(tweet_data):
                                                    new_tweets_found = True
                                                    print(f"new tweet found and saved - {tweet_data['result']['rest_id']}")
                            except Exception as e:
                                print(f"an error has occured! - {e}")
                    except Exception as e:
                        print(f"an error has occured! - {e}")
                if new_tweets_found:
                    self.save_tweets()
            except Exception as e:
                print(f"an error has occured! - {e}")
            finally:
                await browser.close()
    async def run(self):
        print("starting")
        try:
            while True:
                start_time = time.time()
                await self.scrape_tweets()
                elapsed = time.time() - start_time
                sleep_time = max(0, 3 - elapsed)
                await asyncio.sleep(sleep_time)
        except KeyboardInterrupt:
            print("\nstopping...")
async def main():
    scraper = tweet_scraper()
    await scraper.run()
if __name__ == '__main__':
    asyncio.run(main())
