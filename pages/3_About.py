"""
About Page
Project background and methodology
"""
import streamlit as st

st.set_page_config(
    page_title="About | Break-down Breakdown",
    page_icon="ℹ️",
    layout="centered"
)

# Load custom CSS
from pathlib import Path
css_path = Path(__file__).parent.parent / "styles" / "main.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.markdown("""
# About The Break-down Breakdown

## What Is This?

**The Break-down Breakdown** is a free, public dashboard that tracks the health 
of the appliance repair industry in North America.

It combines publicly available economic data with anonymous, crowd-sourced 
insights from working service companies to create something that doesn't 
exist anywhere else: **a real-time pulse on what it's actually like to run 
an appliance repair business right now.**

---

## Why Does This Exist?

Independent appliance repair business owners—especially smaller operators—don't 
have access to the expensive market research that big corporations use to 
make decisions.

Meanwhile, everyone's wondering the same things:
- Is the industry growing or shrinking?
- Are other shops struggling too, or is it just me?
- What's happening with parts availability?
- Should I be hiring or holding off?

We built this to answer those questions with real data.

---

## How It Works

### The Breakdown Index

A single score (0-100) representing overall industry conditions, updated monthly.

| Score | Zone | Meaning |
|-------|------|---------|
| 80-100 | Gravy Train | Peak conditions |
| 60-79 | Humming Along | Solid, no major concerns |
| 40-59 | Check Engine | Mixed signals, some pressure |
| 20-39 | Parts on Backorder | Challenging conditions |
| 0-19 | Total Breakdown | Crisis mode |

### Data Sources

**Economic Indicators (50%)**
- Consumer Confidence Index
- Existing Home Sales
- Mortgage Rates
- Appliance Prices (CPI)

**Industry Metrics (25%)**
- Appliance Shipments
- Technician Wages
- Job Postings

**Field Reports (25%)**
- Anonymous monthly surveys from servicers like you
- Call volume, parts lead times, hiring difficulty, business sentiment

---

## Who's Behind This?

This project was created by appliance repair professionals who wanted 
better data for making business decisions.

We're not selling anything. The dashboard is free. The data is open.

---

## Privacy Commitment

- **Field reports are 100% anonymous**
- No IP addresses logged
- No identifying information collected
- Email signup is optional and stored separately from survey responses
- Regional data only displayed when 10+ responses received (to prevent identification)

---

## Contact

Questions? Suggestions? Corrections?

📧 info@breakdown.report

---

*"Because somebody should be tracking this."*
""")

