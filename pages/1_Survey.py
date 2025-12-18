"""
Field Report Survey Page
Anonymous monthly survey for servicers to contribute real-world data
"""
import streamlit as st
from datetime import datetime
from data.storage import get_storage

st.set_page_config(
    page_title="Submit Field Report | Break-down Breakdown",
    page_icon="📋",
    layout="centered"
)

# Load custom CSS
from pathlib import Path
css_path = Path(__file__).parent.parent / "styles" / "main.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header" style="margin-bottom: 2rem;">
    <h1 style="font-size: 2rem;">📋 Field Report</h1>
    <p class="tagline">Help us track the real state of the industry.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
**Takes 60 seconds. Completely anonymous.**

Your data joins other servicers to create insights nobody else has.
""")

st.divider()

# Survey Form
with st.form("field_report"):
    
    # Q1: Call Volume
    st.markdown("### Call/Lead Volume")
    call_volume = st.radio(
        "Compared to last month, your inbound call/lead volume is:",
        options=[
            "Up significantly (>20%)",
            "Up somewhat (5-20%)",
            "About the same",
            "Down somewhat (5-20%)",
            "Down significantly (>20%)"
        ],
        index=2,
        key="q1"
    )
    
    st.divider()
    
    # Q2: Parts Lead Time
    st.markdown("### Parts Lead Time")
    parts_lead_time = st.slider(
        "What's your average parts lead time right now? (days from order to delivery)",
        min_value=1,
        max_value=60,
        value=7,
        key="q2"
    )
    
    st.divider()
    
    # Q3 & Q4: Hiring
    st.markdown("### Hiring Situation")
    trying_to_hire = st.radio(
        "Are you actively trying to hire technicians?",
        options=["Yes", "No"],
        index=1,
        key="q3"
    )
    
    hiring_difficulty = None
    if trying_to_hire == "Yes":
        hiring_difficulty = st.select_slider(
            "How difficult is it to find qualified candidates?",
            options=[
                "1 - Easy, good candidates available",
                "2 - Manageable, takes some effort",
                "3 - Challenging, limited pool",
                "4 - Very difficult, almost no qualified candidates",
                "5 - Impossible, we've basically given up"
            ],
            value="3 - Challenging, limited pool",
            key="q4"
        )
    
    st.divider()
    
    # Q5: Business Sentiment
    st.markdown("### Overall Business Conditions")
    business_sentiment = st.select_slider(
        "Overall, how would you rate business conditions right now?",
        options=[
            "1 - Brutal (losing money, major stress)",
            "2 - Tough (breaking even, constant pressure)",
            "3 - Okay (making it work, normal challenges)",
            "4 - Good (profitable, manageable stress)",
            "5 - Excellent (crushing it, best it's been)"
        ],
        value="3 - Okay (making it work, normal challenges)",
        key="q5"
    )
    
    st.divider()
    
    # Q6: Region
    st.markdown("### Your Region")
    region = st.selectbox(
        "Where are you located?",
        options=[
            "Northeast",
            "Southeast",
            "Midwest",
            "Southwest",
            "West Coast",
            "Mountain West",
            "Canada"
        ],
        key="q6"
    )
    
    # Q7: Company Size
    st.markdown("### Company Size")
    company_size = st.selectbox(
        "How many people work at your company?",
        options=[
            "Just me (solo operator)",
            "2-5 employees",
            "6-10 employees",
            "11-20 employees",
            "20+ employees"
        ],
        key="q7"
    )
    
    st.divider()
    
    # Submit
    submitted = st.form_submit_button(
        "Submit Field Report",
        use_container_width=True,
        type="primary"
    )
    
    if submitted:
        # Convert responses to numeric values for storage
        call_volume_map = {
            "Up significantly (>20%)": 5,
            "Up somewhat (5-20%)": 4,
            "About the same": 3,
            "Down somewhat (5-20%)": 2,
            "Down significantly (>20%)": 1
        }
        
        sentiment_map = {
            "1 - Brutal (losing money, major stress)": 1,
            "2 - Tough (breaking even, constant pressure)": 2,
            "3 - Okay (making it work, normal challenges)": 3,
            "4 - Good (profitable, manageable stress)": 4,
            "5 - Excellent (crushing it, best it's been)": 5
        }
        
        difficulty_map = {
            "1 - Easy, good candidates available": 1,
            "2 - Manageable, takes some effort": 2,
            "3 - Challenging, limited pool": 3,
            "4 - Very difficult, almost no qualified candidates": 4,
            "5 - Impossible, we've basically given up": 5
        }
        
        report_data = {
            'call_volume': call_volume_map.get(call_volume, 3),
            'parts_lead_time': parts_lead_time,
            'trying_to_hire': trying_to_hire == "Yes",
            'hiring_difficulty': difficulty_map.get(hiring_difficulty, None) if hiring_difficulty else None,
            'business_sentiment': sentiment_map.get(business_sentiment, 3),
            'region': region,
            'company_size': company_size,
            'month': datetime.now().strftime('%Y-%m')
        }
        
        # Save to database
        storage = get_storage()
        saved = storage.save_field_report(report_data)
        
        if saved:
            st.success("✅ Your field report has been received!")
        else:
            st.warning("⚠️ Report saved locally. Database sync pending.")
        
        st.balloons()
        
        st.markdown("""
        ---
        
        ### Thank you for contributing!
        
        Your anonymous data helps fellow servicers understand the bigger picture.
        """)
        
        # Optional email signup
        st.markdown("### Want the monthly report?")
        email = st.text_input(
            "Drop your email (optional):",
            placeholder="you@example.com",
            key="email_signup"
        )
        
        if email:
            # TODO: Save email to separate table
            st.info("📧 We'll send you the monthly breakdown!")
        
        # Link back to dashboard
        if st.button("← Back to Dashboard"):
            st.switch_page("app.py")

