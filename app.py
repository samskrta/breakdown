"""
The Break-down Breakdown
A Real-Time Industry Health Dashboard for Appliance Repair Professionals
"""
import streamlit as st
from components.gauge import render_gauge
from components.error_codes import render_error_codes
from components.trend_sparkline import render_sparkline
from components.survey import render_survey_cta
from components.appliance_icons import render_header_with_icons, render_appliance_strip
from components.news_feed import render_news_feed
from data.index_calculator import get_current_index, get_index_history
from data.error_code_engine import get_active_error_codes

# Page config
st.set_page_config(
    page_title="The Break-down Breakdown",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open("styles/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header with appliance icons
render_header_with_icons()

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    # The Main Gauge
    current_index = get_current_index()
    render_gauge(current_index['score'], current_index['change'])
    
    # Sparkline trend
    history = get_index_history()
    render_sparkline(history)

with col2:
    # Error Codes Panel
    error_codes = get_active_error_codes()
    render_error_codes(error_codes)
    
    # Survey CTA
    render_survey_cta()

# Appliance strip divider
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
render_appliance_strip()

# News Feed Section
st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
render_news_feed()

# Footer
st.markdown("""
<div class="footer">
    <p>Based on data from <strong>147</strong> field reports this month</p>
    <p class="last-updated">Last updated: December 18, 2025</p>
</div>
""", unsafe_allow_html=True)
