"""
The Break-down Breakdown
A Real-Time Industry Health Dashboard for Appliance Repair Professionals
"""
import streamlit as st
from components.gauge import render_gauge
from components.error_codes import render_error_codes
from components.trend_sparkline import render_sparkline
from components.survey import render_survey_cta
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

# Header
st.markdown("""
<div class="header">
    <h1 class="title">The Break-down Breakdown</h1>
    <p class="tagline">The breakdown on the stuff that breaks down.</p>
</div>
""", unsafe_allow_html=True)

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

# Footer
st.markdown("""
<div class="footer">
    <p>Based on data from <strong>147</strong> field reports this month</p>
    <p class="last-updated">Last updated: December 18, 2025</p>
</div>
""", unsafe_allow_html=True)

