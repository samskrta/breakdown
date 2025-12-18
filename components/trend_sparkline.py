"""
Trend Sparkline Component
Shows 12-month index history as a compact line chart
"""
import streamlit as st
import plotly.graph_objects as go
from typing import List, Dict


def render_sparkline(history: List[Dict]):
    """
    Render a sparkline showing index trend over time
    
    Args:
        history: List of dicts with 'month' and 'score' keys
    """
    if not history:
        return
    
    months = [h['month'] for h in history]
    scores = [h['score'] for h in history]
    
    # Determine color based on trend
    if len(scores) >= 2:
        trend_color = "#6B8E23" if scores[-1] >= scores[-2] else "#B7410E"
    else:
        trend_color = "#4A4A4A"
    
    fig = go.Figure()
    
    # Area fill
    fig.add_trace(go.Scatter(
        x=months,
        y=scores,
        fill='tozeroy',
        fillcolor=f'rgba({int(trend_color[1:3], 16)}, {int(trend_color[3:5], 16)}, {int(trend_color[5:7], 16)}, 0.1)',
        line=dict(color=trend_color, width=2),
        mode='lines',
        hovertemplate='%{x}<br>Score: %{y}<extra></extra>'
    ))
    
    # Current point marker
    fig.add_trace(go.Scatter(
        x=[months[-1]],
        y=[scores[-1]],
        mode='markers',
        marker=dict(size=10, color=trend_color, symbol='circle'),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=80,
        margin=dict(l=0, r=0, t=10, b=20),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            tickfont=dict(size=10, family='IBM Plex Mono', color='#4A4A4A'),
            tickangle=-45,
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, 100]
        ),
    )
    
    st.markdown('<div class="sparkline-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

