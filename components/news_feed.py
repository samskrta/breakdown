"""
News Feed Component
Industry news and updates section
"""
import streamlit as st
from typing import List, Dict
from datetime import datetime, timedelta


def get_news_items() -> List[Dict]:
    """
    Get news items for the feed.
    TODO: Connect to RSS feeds or news API
    """
    # Mock news for now - would be replaced with actual RSS/API
    today = datetime.now()
    
    return [
        {
            'title': 'Right to Repair Gains Momentum in California',
            'source': 'Repair.org',
            'date': (today - timedelta(days=1)).strftime('%b %d'),
            'url': '#',
            'category': 'legislation',
            'icon': '⚖️'
        },
        {
            'title': 'Samsung Extends Parts Availability for Major Appliances',
            'source': 'Appliance Service News',
            'date': (today - timedelta(days=2)).strftime('%b %d'),
            'url': '#',
            'category': 'parts',
            'icon': '🔧'
        },
        {
            'title': 'Technician Shortage Hits Record Levels in Midwest',
            'source': 'UASA Weekly',
            'date': (today - timedelta(days=3)).strftime('%b %d'),
            'url': '#',
            'category': 'labor',
            'icon': '👷'
        },
        {
            'title': 'Whirlpool Announces New Diagnostic Tool Program',
            'source': 'Appliance Design',
            'date': (today - timedelta(days=5)).strftime('%b %d'),
            'url': '#',
            'category': 'tools',
            'icon': '📱'
        },
        {
            'title': 'Home Appliance Shipments Down 8% in Q4',
            'source': 'AHAM',
            'date': (today - timedelta(days=7)).strftime('%b %d'),
            'url': '#',
            'category': 'market',
            'icon': '📊'
        },
    ]


def render_news_feed():
    """Render the industry news feed section"""
    news_items = get_news_items()
    
    st.markdown('''
    <div class="news-section">
        <div class="news-header">
            <h2 class="news-title">📰 Industry Wire</h2>
            <span class="news-subtitle">What's happening in the appliance repair world</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # News grid
    cols = st.columns(len(news_items))
    
    for i, item in enumerate(news_items):
        with cols[i]:
            st.markdown(f'''
            <div class="news-card">
                <div class="news-icon">{item['icon']}</div>
                <div class="news-date">{item['date']}</div>
                <div class="news-card-title">{item['title']}</div>
                <div class="news-source">{item['source']}</div>
            </div>
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

