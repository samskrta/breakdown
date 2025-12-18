"""
Survey/Field Report Components
CTA button and embedded survey form
"""
import streamlit as st


def render_survey_cta():
    """Render the call-to-action to submit a field report"""
    st.markdown("""
    <div class="survey-cta" onclick="window.location.href='Survey'">
        <h3>📋 Submit Your Field Report</h3>
        <p>Takes 60 seconds. Help track the real state of the industry.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Streamlit button fallback for navigation
    if st.button("Submit Field Report →", key="survey_cta_btn", use_container_width=True):
        st.switch_page("pages/1_Survey.py")


def render_survey_stats(total_reports: int, this_month: int):
    """Show survey participation stats"""
    st.markdown(f"""
    <div class="survey-stats">
        <div class="stat">
            <span class="stat-value">{total_reports:,}</span>
            <span class="stat-label">Total Field Reports</span>
        </div>
        <div class="stat">
            <span class="stat-value">{this_month}</span>
            <span class="stat-label">This Month</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

