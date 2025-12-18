"""
Deep Dive Page
Detailed breakdown of all indicators contributing to the index
"""
import streamlit as st
import plotly.graph_objects as go
from data.fred_client import get_fred_client, FRED_SERIES

st.set_page_config(
    page_title="Deep Dive | Break-down Breakdown",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
from pathlib import Path
css_path = Path(__file__).parent.parent / "styles" / "main.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header" style="margin-bottom: 2rem;">
    <h1 style="font-size: 2rem;">📊 The Deep Dive</h1>
    <p class="tagline">Every data point behind the Breakdown Index.</p>
</div>
""", unsafe_allow_html=True)

# Tabs for sections
tab1, tab2, tab3 = st.tabs(["Economic Indicators", "Industry Metrics", "Field Reports"])

with tab1:
    st.markdown("## Economic Indicators")
    st.markdown("*Data from Federal Reserve Economic Data (FRED)*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Consumer Confidence")
        st.metric(
            label="U of Michigan Consumer Sentiment",
            value="68.5",
            delta="-2.1 from last month"
        )
        st.caption("""
        **What it means:** Consumer confidence affects spending decisions. 
        When confidence is lower, people repair instead of replace.
        """)
        
        st.markdown("### 30-Year Mortgage Rate")
        st.metric(
            label="Weekly Average",
            value="6.8%",
            delta="+0.2%",
            delta_color="inverse"
        )
        st.caption("""
        **What it means:** Higher rates = less home turnover = more repairs. 
        People stay put and maintain what they have.
        """)
    
    with col2:
        st.markdown("### Existing Home Sales")
        st.metric(
            label="Annual Rate (Millions)",
            value="4.1M",
            delta="-0.3M from last month"
        )
        st.caption("""
        **What it means:** Low turnover is good for repair. 
        New homeowners often replace; long-term owners repair.
        """)
        
        st.markdown("### Major Appliance CPI")
        st.metric(
            label="Price Index",
            value="108.5",
            delta="+1.2"
        )
        st.caption("""
        **What it means:** Rising new appliance prices make repair more attractive. 
        Consumers do the math.
        """)

with tab2:
    st.markdown("## Industry-Specific Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Appliance Shipments")
        st.metric(
            label="AHAM Monthly (Millions)",
            value="8.2M",
            delta="-0.5M"
        )
        st.caption("""
        **What it means:** Lower shipments = less replacement activity = more repair demand.
        """)
        
        st.markdown("### Job Posting Volume")
        st.metric(
            label="Repair Tech Listings (Index)",
            value="62",
            delta="+8"
        )
        st.caption("""
        **What it means:** More job postings = tighter labor market = harder to hire.
        """)
    
    with col2:
        st.markdown("### Tech Wage Growth")
        st.metric(
            label="YoY Change",
            value="+4.5%",
            delta="+0.5%"
        )
        st.caption("""
        **What it means:** Wage pressure indicates competition for talent.
        """)
        
        st.markdown("### Right to Repair Progress")
        st.info("🔧 **2 states** passed R2R legislation this year")
        st.caption("""
        **What it means:** Expanding access to parts, manuals, and diagnostic tools.
        """)

with tab3:
    st.markdown("## Field Report Data")
    st.markdown("*Crowd-sourced from working servicers like you*")
    
    st.info("📊 **Based on 147 field reports this month**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Call Volume Sentiment")
        
        # Mock distribution chart
        fig = go.Figure(go.Bar(
            x=['Down a lot', 'Down some', 'Same', 'Up some', 'Up a lot'],
            y=[8, 22, 45, 67, 12],
            marker_color=['#B7410E', '#CC5500', '#DAA520', '#8FBC8F', '#6B8E23']
        ))
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=20, b=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric(
            label="Average Score",
            value="3.4 / 5",
            delta="Stable demand"
        )
        
        st.markdown("### Hiring Difficulty")
        st.metric(
            label="Average Score (1=Easy, 5=Impossible)",
            value="3.8",
            delta="+0.3",
            delta_color="inverse"
        )
        st.caption("Getting harder to find qualified techs.")
    
    with col2:
        st.markdown("### Parts Lead Time")
        st.metric(
            label="Average Days",
            value="8.5",
            delta="-1.2"
        )
        st.progress(0.28, text="Within normal range (1-30 days)")
        
        st.markdown("### Business Sentiment")
        st.metric(
            label="Average Score (1=Brutal, 5=Excellent)",
            value="3.2",
            delta="+0.1"
        )
        st.caption("Most servicers report 'okay' to 'good' conditions.")

st.divider()

# Methodology link
with st.expander("📖 Methodology & Data Sources"):
    st.markdown("""
    ### How the Breakdown Index is Calculated
    
    The Breakdown Index is a weighted composite of three data categories:
    
    **Economic Indicators (50% weight)**
    - Consumer Confidence Index (10%)
    - Existing Home Sales (15%) - *inverse: lower turnover = higher score*
    - 30-Year Mortgage Rate (10%)
    - Major Appliance CPI (15%)
    
    **Industry Metrics (25% weight)**
    - Appliance Shipments (10%) - *inverse: lower = higher score*
    - Tech Wage Growth (5%) - *inverse*
    - Job Posting Volume (5%) - *inverse*
    - Parts Availability (5%)
    
    **Field Report Data (25% weight)**
    - Call Volume Sentiment (10%)
    - Parts Lead Time (5%) - *inverse*
    - Hiring Difficulty (5%) - *inverse*
    - Business Sentiment (5%)
    
    Each indicator is normalized to a 0-100 scale based on historical ranges, 
    then weighted and summed.
    
    ### Data Sources
    - **FRED API**: Consumer Confidence, Home Sales, Mortgage Rates, CPI
    - **AHAM**: Appliance shipment reports
    - **BLS**: Wage data
    - **Anonymous Survey**: Field reports from servicers
    
    ### Privacy
    - Field report responses are completely anonymous
    - No IP addresses are logged
    - Regional data only shown when 10+ responses received
    """)

