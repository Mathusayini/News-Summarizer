import os
import requests
from bs4 import BeautifulSoup
from llm_client import LLM
from dotenv import load_dotenv
import sqlite3
import json
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import feedparser
import re
from collections import Counter
import nltk

# Download NLTK tokenizer
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Load environment variables
load_dotenv()

@dataclass
class NewsArticle:
    title: str
    content: str
    summary: str
    keywords: List[str]
    sentiment: str
    source: str
    url: str

    def to_dict(self):
        return {
            'title': self.title,
            'summary': self.summary,
            'keywords': self.keywords,
            'sentiment': self.sentiment,
            'source': self.source,
            'url': self.url
        }

class NewsSummarizer:
    def __init__(self):
        print("[DEBUG] Initializing NewsSummarizer...")
        self.setup_database()
        self.setup_gemini()
        self.news_sources = {
            'guardian': 'https://www.theguardian.com/world/rss',
            'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            'reuters': 'http://feeds.reuters.com/reuters/topNews',
            'techcrunch': 'https://techcrunch.com/feed/',
        }

    def setup_database(self):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                title TEXT,
                summary TEXT,
                keywords TEXT,
                sentiment TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("[DEBUG] Database setup complete.")

    def setup_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file")
        self.model = LLM()
        print("[DEBUG] Gemini setup complete.")

    def get_article_text(self, url: str) -> tuple:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, "lxml")
            title = soup.title.get_text().strip() if soup.title else "Untitled"
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            content = ' '.join(paragraphs)
            return title, content
        except Exception as e:
            print(f"❌ Error fetching article: {e}")
            return None, None

    def summarize_with_gemini(self, text: str) -> str:
        try:
            prompt = f"Summarize this news article in 3-4 sentences:\n\n{text[:5000]}"
            response = self.model.ask(prompt)
            if not response or not response:
                print("❌ QWEN returned an empty response.")
                return "Summary unavailable"
            return response.strip()
        except Exception as e:
            print(f"❌ QWEN error: {e}")
            return "Summary unavailable"

    def extract_keywords(self, text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stopwords = {'that', 'with', 'have', 'this', 'will', 'been', 'their', 'said', 'each', 'which', 'from', 'they', 'more'}
        words = [w for w in words if w not in stopwords]
        return [word for word, count in Counter(words).most_common(5)]

    def analyze_sentiment(self, text: str) -> str:
        try:
            prompt = f"What is the sentiment of this text? Reply with only: positive, negative, or neutral\n\n{text[:1000]}"
            response = self.model.generate_content(prompt)
            sentiment = response.text.strip().lower()
            return sentiment if sentiment in ['positive', 'negative', 'neutral'] else 'neutral'
        except:
            return 'neutral'
    def process_rss_feed(self, rss_url: str, max_articles: int = 5) -> List[NewsArticle]:
        """Process articles from an RSS feed"""
        print(f"[DEBUG] Fetching RSS feed: {rss_url}")
        try:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                print("❌ No articles found in RSS feed.")
                return []
            
            articles = []
            source_name = feed.feed.get('title', 'RSS Feed')
            print(f"[DEBUG] Found {len(feed.entries)} articles in feed: {source_name}")
            
            for i, entry in enumerate(feed.entries[:max_articles]):
                print(f"[DEBUG] Processing article {i+1}/{min(max_articles, len(feed.entries))}: {entry.title[:50]}...")
                article = self.process_article(entry.link, source_name)
                if article:
                    articles.append(article)
            
            return articles
        except Exception as e:
            print(f"❌ Error processing RSS feed: {e}")
            return []

    def process_article(self, url: str, source: str = "manual") -> Optional[NewsArticle]:
        print("[DEBUG] Fetching article...")
        title, content = self.get_article_text(url)
        if not title or not content or len(content) < 100:
            print("❌ Article content too short or invalid.")
            return None
        print("[DEBUG] Summarizing article...")
        summary = self.summarize_with_gemini(content)
        keywords = self.extract_keywords(content)
        sentiment = self.analyze_sentiment(content)
        return NewsArticle(title, content, summary, keywords, sentiment, source, url)

    def save_article(self, article: NewsArticle):
        conn = sqlite3.connect('news.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (url, title, summary, keywords, sentiment, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                article.url, article.title, article.summary,
                json.dumps(article.keywords), article.sentiment, article.source
            ))
            conn.commit()
            print(f"✅ Saved: {article.title[:50]}...")
        except Exception as e:
            print(f"❌ Save error: {e}")
        finally:
            conn.close()

# Entry point
def main():
    summarizer = NewsSummarizer()
    print("\n🧠 News Summarizer with Gemini AI")
    print("Enter a news URL to summarize it, or type 'quit' to exit.")

    while True:
        user_input = input("\n🔗 Enter URL (or 'quit'): ").strip()

        if user_input.lower() in ['quit', 'exit']:
            print("👋 Exiting. Goodbye!")
            break

        if not user_input.startswith("http"):
            print("❌ Please enter a valid URL starting with 'http'")
            continue

                # Check if it's an RSS feed URL
        if any(keyword in user_input.lower() for keyword in ['rss', 'feed', '.xml']) or user_input.endswith('/rss'):
            print("📡 Detected RSS feed URL. Processing multiple articles...")
            articles = summarizer.process_rss_feed(user_input)
            if articles:
                print(f"\n✅ Successfully processed {len(articles)} articles from RSS feed!")
                for i, article in enumerate(articles, 1):
                    summarizer.save_article(article)
                    print(f"\n--- Article {i} ---")
                    print(f"✅ Title: {article.title}")
                    print(f"🎭 Sentiment: {article.sentiment}")
                    print(f"🏷️ Keywords: {', '.join(article.keywords)}")
                    print(f"📄 Summary: {article.summary}")
                    print(f"🔗 URL: {article.url}")
            else:
                print("❌ Failed to process RSS feed. Try another URL.")
        else:
            # Process single article
            article = summarizer.process_article(user_input)
            if article:
                summarizer.save_article(article)
                print(f"\n✅ Title: {article.title}")
                print(f"🎭 Sentiment: {article.sentiment}")
                print(f"🏷️ Keywords: {', '.join(article.keywords)}")
                print(f"\n📄 Summary:\n{article.summary}")
            else:
                print("❌ Failed to summarize. Try another URL.")


if __name__ == "__main__":
    main()

