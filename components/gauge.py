"""
The Breakdown Index Gauge Component
A vintage-style dial displaying the composite industry health score
"""
import streamlit as st
import plotly.graph_objects as go


def get_zone_info(score: float) -> dict:
    """Get zone name and color based on score"""
    if score >= 80:
        return {"name": "Gravy Train", "color": "#6B8E23", "class": "gravy-train"}
    elif score >= 60:
        return {"name": "Humming Along", "color": "#8FBC8F", "class": "humming"}
    elif score >= 40:
        return {"name": "Check Engine", "color": "#DAA520", "class": "check-engine"}
    elif score >= 20:
        return {"name": "Parts on Backorder", "color": "#CC5500", "class": "backorder"}
    else:
        return {"name": "Total Breakdown", "color": "#B7410E", "class": "breakdown"}


def render_gauge(score: float, change: float = 0):
    """
    Render the main Breakdown Index gauge
    
    Args:
        score: Current index score (0-100)
        change: Change from last month (positive or negative)
    """
    zone = get_zone_info(score)
    
    # Create the gauge using Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'font': {'size': 72, 'family': 'IBM Plex Mono', 'color': '#2D2D2D'},
            'suffix': '',
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 2,
                'tickcolor': '#4A4A4A',
                'tickfont': {'size': 14, 'family': 'Barlow Condensed'},
                'tickmode': 'array',
                'tickvals': [0, 20, 40, 60, 80, 100],
                'ticktext': ['0', '20', '40', '60', '80', '100'],
            },
            'bar': {'color': '#8B0000', 'thickness': 0.15},
            'bgcolor': '#F5F2EB',
            'borderwidth': 3,
            'bordercolor': '#4A4A4A',
            'steps': [
                {'range': [0, 20], 'color': '#B7410E'},    # Total Breakdown
                {'range': [20, 40], 'color': '#CC5500'},   # Parts on Backorder
                {'range': [40, 60], 'color': '#DAA520'},   # Check Engine
                {'range': [60, 80], 'color': '#8FBC8F'},   # Humming Along
                {'range': [80, 100], 'color': '#6B8E23'},  # Gravy Train
            ],
            'threshold': {
                'line': {'color': '#8B0000', 'width': 6},
                'thickness': 0.85,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'IBM Plex Mono'},
        height=350,
        margin=dict(l=30, r=30, t=50, b=30),
    )
    
    # Render the gauge
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Zone label and change indicator
    change_class = "up" if change >= 0 else "down"
    change_symbol = "↑" if change >= 0 else "↓"
    change_text = f"{change_symbol} {abs(change):.1f} from last month"
    
    st.markdown(f"""
    <div class="score-display">
        <div class="score-label">
            <span class="zone-label {zone['class']}">{zone['name']}</span>
        </div>
        <div class="score-change {change_class}">{change_text}</div>
    </div>
    """, unsafe_allow_html=True)

