"""
News Feed Component
Industry news from RSS feeds
"""
import streamlit as st
from typing import List, Dict
from datetime import datetime
import feedparser
import requests
from urllib.parse import quote

# RSS Feed sources for appliance repair industry
RSS_FEEDS = [
    {
        'name': 'Repair.org',
        'url': 'https://www.repair.org/blog?format=rss',
        'icon': '⚖️',
        'category': 'legislation'
    },
    {
        'name': 'Appliance Service News',
        'url': 'https://www.applianceservicenews.com/feed/',
        'icon': '🔧',
        'category': 'industry'
    },
]

# Google News RSS as fallback/supplement
GOOGLE_NEWS_TOPICS = [
    ('appliance repair industry', '🔧'),
    ('right to repair appliance', '⚖️'),
    ('appliance technician shortage', '👷'),
]


def get_google_news_rss(query: str) -> str:
    """Generate Google News RSS URL for a search query"""
    encoded_query = quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_rss_feed(url: str, source_name: str, icon: str) -> List[Dict]:
    """Fetch and parse an RSS feed"""
    try:
        feed = feedparser.parse(url)
        items = []
        
        for entry in feed.entries[:3]:  # Get top 3 from each source
            # Parse date
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                date = datetime(*entry.published_parsed[:6])
                date_str = date.strftime('%b %d')
            else:
                date_str = 'Recent'
            
            items.append({
                'title': entry.title[:80] + '...' if len(entry.title) > 80 else entry.title,
                'url': entry.link,
                'source': source_name,
                'date': date_str,
                'icon': icon
            })
        
        return items
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []


@st.cache_data(ttl=3600)
def get_news_items() -> List[Dict]:
    """
    Get news items from multiple RSS feeds
    """
    all_items = []
    
    # Fetch from configured RSS feeds
    for feed in RSS_FEEDS:
        items = fetch_rss_feed(feed['url'], feed['name'], feed['icon'])
        all_items.extend(items)
    
    # Fetch from Google News for industry topics
    for topic, icon in GOOGLE_NEWS_TOPICS:
        url = get_google_news_rss(topic)
        items = fetch_rss_feed(url, 'Industry News', icon)
        all_items.extend(items[:2])  # Limit Google News items
    
    # If no items fetched, return fallback
    if not all_items:
        return get_fallback_news()
    
    # Remove duplicates by title and limit to 5
    seen_titles = set()
    unique_items = []
    for item in all_items:
        title_key = item['title'][:40].lower()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_items.append(item)
    
    return unique_items[:5]


def get_fallback_news() -> List[Dict]:
    """Fallback news items if RSS fails"""
    return [
        {
            'title': 'Visit Repair.org for Right to Repair news',
            'source': 'Repair.org',
            'date': '',
            'url': 'https://www.repair.org',
            'icon': '⚖️'
        },
        {
            'title': 'AHAM Appliance Industry Updates',
            'source': 'AHAM',
            'date': '',
            'url': 'https://www.aham.org',
            'icon': '📊'
        },
        {
            'title': 'Appliance Service News',
            'source': 'ASN',
            'date': '',
            'url': 'https://www.applianceservicenews.com',
            'icon': '🔧'
        },
    ]


def render_news_feed():
    """Render the industry news feed section"""
    news_items = get_news_items()
    
    st.markdown('''
    <div class="news-section">
        <div class="news-header">
            <h2 class="news-title">📰 Industry Wire</h2>
            <span class="news-subtitle">Live headlines from the appliance repair world</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # News grid
    cols = st.columns(len(news_items))
    
    for i, item in enumerate(news_items):
        with cols[i]:
            st.markdown(f'''
            <a href="{item['url']}" target="_blank" class="news-card-link">
                <div class="news-card">
                    <div class="news-icon">{item['icon']}</div>
                    <div class="news-date">{item['date']}</div>
                    <div class="news-card-title">{item['title']}</div>
                    <div class="news-source">{item['source']}</div>
                </div>
            </a>
            ''', unsafe_allow_html=True)


def render_news_ticker():
    """Render a scrolling news ticker"""
    news_items = get_news_items()
    ticker_items = ' • '.join([f"{n['icon']} {n['title']}" for n in news_items])
    
    st.markdown(f'''
    <div class="news-ticker-container">
        <div class="news-ticker">
            <span class="ticker-content">{ticker_items} • {ticker_items}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
