"""
Error Codes Panel Component
Displays current "diagnostic codes" affecting the industry
"""
import streamlit as st
from typing import List, Dict


def render_error_codes(codes: List[Dict]):
    """
    Render the error codes panel
    
    Args:
        codes: List of error code dictionaries with keys:
            - code: The error code ID (e.g., "E7")
            - name: Short identifier (e.g., "TECH_SHORTAGE_DETECTED")
            - message: Human-readable description
            - severity: "warning" or "good"
    """
    st.markdown("""
    <div class="error-codes-panel">
        <div class="error-codes-title">Current Diagnostics</div>
    """, unsafe_allow_html=True)
    
    for code in codes:
        icon = "⚠️" if code['severity'] == "warning" else "✓"
        icon_class = code['severity']
        
        st.markdown(f"""
        <div class="error-code">
            <span class="error-code-icon {icon_class}">{icon}</span>
            <span class="error-code-id">{code['code']}:</span>
            <span class="error-code-desc">{code['name']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_error_code_detail(code: Dict):
    """
    Render expanded detail for a single error code
    Used when user clicks to expand
    """
    with st.expander(f"{code['code']}: {code['name']}", expanded=False):
        st.markdown(f"**{code['message']}**")
        if 'data_points' in code:
            for point in code['data_points']:
                st.markdown(f"- {point}")
        if 'recommendation' in code:
            st.info(f"💡 {code['recommendation']}")

