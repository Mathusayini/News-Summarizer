# 📰 News Summarizer with Qwen AI via OpenRouter

A Python-based AI-powered news summarizer that leverages the powerful **Qwen-2.5-72B-Instruct** model through OpenRouter to intelligently process and analyze news content.

## ✨ Key Features

- 🔎 **Multi-source content fetching** - Process individual article URLs or entire RSS feeds
- 🤖 **AI-powered summarization** - Utilizes Qwen-2.5-72B-Instruct via OpenRouter for high-quality summaries
- 🧠 **Smart keyword extraction** - Automatically identifies the top 5 most relevant keywords
- 📊 **Sentiment analysis** - Determines emotional tone (positive, negative, or neutral)
- 🗃️ **Persistent storage** - Saves all data in a structured SQLite database
- 🔐 **Secure configuration** - Environment-based API key management

---

## 🔧 Prerequisites

- **Python 3.8+**
- **OpenRouter API key** - Get yours at [openrouter.ai](https://openrouter.ai/)
- **Internet connection** for fetching articles and API requests

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news-summarizer.git
cd news-summarizer
```

### 2. Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Important:** Make sure `.env` is added to your `.gitignore` file:

```gitignore
# Environment variables
.env

# Database
news.db

# Python cache
__pycache__/
*.pyc
```

---

## 💻 Usage

### Summarize a Single Article

```bash
python summarize.py --url "https://example.com/news/article"
```

### Process an Entire RSS Feed

```bash
python summarize.py --rss "https://example.com/rss-feed"
```

### View Help and Options

```bash
python summarize.py --help
```

---

## 📊 Output & Storage

All processed data is automatically stored in `news.db` (SQLite database) with the following structure:

| Field | Type | Description |
|-------|------|-------------|
| title | TEXT | Article headline |
| summary | TEXT | AI-generated summary |
| keywords | TEXT | Top 5 extracted keywords |
| sentiment | TEXT | Sentiment analysis result |
| url | TEXT | Source URL |
| timestamp | DATETIME | Processing time |



## 🔧 Technical Stack

### AI/ML Components
- **Qwen-2.5-72B-Instruct** (via OpenRouter) - Primary summarization model
- **NLTK** - Natural language processing for keyword extraction
- **TextBlob/VADER** - Sentiment analysis

### Core Libraries
- **requests** - HTTP requests for fetching content
- **feedparser** - RSS feed parsing
- **beautifulsoup4** - HTML content extraction
- **sqlite3** - Database operations
- **python-dotenv** - Environment variable management

---

## 🛡️ Environment Variables

Your `.env` file should contain:

```env
# Required: OpenRouter API access
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional: Alternative model support (if implemented)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Database configuration
DATABASE_PATH=news.db
```

---

