import feedparser
from textblob import TextBlob
import random

class NewsAgent:
    def __init__(self):
        # REAL Nigerian News Feeds
        self.sources = [
            "https://rss.punchng.com/v1/category/latest_news",
            "https://www.vanguardngr.com/feed",
            "https://cointelegraph.com/rss" # For Crypto Panic
        ]
        self.panic_words = ["crisis", "kill", "explosion", "collapse", "strike", "protest", "crash", "scarcity", "fuel"]

    def scan_network(self):
        """
        Scrapes news for panic signals.
        Returns: { 'panic_factor': 0.0-1.0, 'headline': str }
        """
        try:
            # Pick a random source to keep it fast
            source = random.choice(self.sources)
            feed = feedparser.parse(source)
            
            if not feed.entries:
                return {"panic_factor": 0.2, "headline": "NO SIGNAL: Systems Nominal"}

            # Analyze the top 3 headlines
            panic_score = 0.0
            top_headline = feed.entries[0].title

            for entry in feed.entries[:3]:
                text = entry.title.lower()
                blob = TextBlob(text)
                
                # 1. Sentiment Analysis (Polarity: -1 is Bad, +1 is Good)
                sentiment = blob.sentiment.polarity
                if sentiment < -0.1: 
                    panic_score += 0.2
                
                # 2. Keyword Search
                for word in self.panic_words:
                    if word in text:
                        panic_score += 0.3
                        top_headline = f"ALERT: {entry.title}"
            
            # Cap the score at 100% (1.0)
            final_score = min(0.99, max(0.1, panic_score))
            
            return {
                "panic_factor": final_score, 
                "headline": top_headline
            }

        except Exception as e:
            return {"panic_factor": 0.0, "headline": "OFFLINE: Satellite Link Broken"}