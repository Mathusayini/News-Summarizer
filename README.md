# 📰 News Summarizer with Qwen AI via OpenRouter

This is a Python-based AI-powered news summarizer that can:
- Fetch news content from individual article URLs or RSS feeds
- Summarize the content using the **Qwen-2.5-72B-Instruct** model via **OpenRouter**
- Extract keywords
- Analyze the sentiment
- Store structured data in an SQLite database

---

## 🔧 Features

✅ Summarizes long news articles using an advanced LLM  
✅ Extracts the top 5 keywords from the article  
✅ Analyzes sentiment (positive, negative, or neutral)  
✅ Supports both single article URLs and RSS feeds  
✅ Stores all results in a local SQLite database (`news.db`)  
✅ Uses `.env` file to keep API key secure  

---

## 📦 Requirements

- Python 3.8 or newer
- An API key from [OpenRouter](https://openrouter.ai/)
- Internet connection

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/news-summarizer.git
cd news-summarizer
