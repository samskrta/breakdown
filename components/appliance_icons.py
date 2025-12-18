"""
Appliance Icons Component
SVG icons for visual flair
"""
import streamlit as st

# Appliance SVG icons - vintage/retro style
APPLIANCES = {
    'washer': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="8" y="4" width="48" height="56" rx="4" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <circle cx="32" cy="38" r="16" fill="none" stroke="#4A4A4A" stroke-width="2"/>
        <circle cx="32" cy="38" r="12" fill="#DAA520" opacity="0.3"/>
        <circle cx="32" cy="38" r="6" fill="#4A4A4A"/>
        <rect x="14" y="10" width="8" height="8" rx="2" fill="#6B8E23"/>
        <rect x="26" y="10" width="8" height="8" rx="2" fill="#CC5500"/>
        <circle cx="48" cy="14" r="4" fill="#4A4A4A"/>
    </svg>
    ''',
    'dryer': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="8" y="4" width="48" height="56" rx="4" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <circle cx="32" cy="38" r="16" fill="none" stroke="#4A4A4A" stroke-width="2"/>
        <circle cx="32" cy="38" r="12" fill="#8FBC8F" opacity="0.3"/>
        <path d="M26 32 Q32 28 38 32 Q32 36 26 32" fill="#4A4A4A"/>
        <path d="M26 38 Q32 34 38 38 Q32 42 26 38" fill="#4A4A4A"/>
        <path d="M26 44 Q32 40 38 44 Q32 48 26 44" fill="#4A4A4A"/>
        <rect x="14" y="10" width="36" height="6" rx="2" fill="#4A4A4A"/>
    </svg>
    ''',
    'fridge': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="12" y="2" width="40" height="60" rx="3" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <line x1="12" y1="22" x2="52" y2="22" stroke="#4A4A4A" stroke-width="2"/>
        <rect x="44" y="8" width="4" height="8" rx="1" fill="#4A4A4A"/>
        <rect x="44" y="28" width="4" height="12" rx="1" fill="#4A4A4A"/>
        <circle cx="26" cy="12" r="3" fill="#6B8E23"/>
        <rect x="18" y="30" width="12" height="8" rx="1" fill="#DAA520" opacity="0.5"/>
        <rect x="18" y="42" width="8" height="6" rx="1" fill="#CC5500" opacity="0.5"/>
    </svg>
    ''',
    'dishwasher': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="8" y="4" width="48" height="56" rx="4" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <line x1="8" y1="16" x2="56" y2="16" stroke="#4A4A4A" stroke-width="2"/>
        <rect x="14" y="8" width="6" height="4" rx="1" fill="#6B8E23"/>
        <rect x="24" y="8" width="6" height="4" rx="1" fill="#CC5500"/>
        <circle cx="48" cy="10" r="3" fill="#4A4A4A"/>
        <rect x="16" y="24" width="32" height="4" rx="1" fill="#4A4A4A" opacity="0.3"/>
        <rect x="16" y="32" width="32" height="4" rx="1" fill="#4A4A4A" opacity="0.3"/>
        <rect x="16" y="40" width="32" height="4" rx="1" fill="#4A4A4A" opacity="0.3"/>
        <rect x="28" y="50" width="8" height="6" rx="1" fill="#4A4A4A"/>
    </svg>
    ''',
    'oven': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="8" y="4" width="48" height="56" rx="4" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <rect x="14" y="20" width="36" height="34" rx="2" fill="none" stroke="#4A4A4A" stroke-width="2"/>
        <rect x="18" y="24" width="28" height="26" fill="#2D2D2D" opacity="0.8"/>
        <circle cx="20" cy="12" r="3" fill="#B7410E"/>
        <circle cx="32" cy="12" r="3" fill="#B7410E"/>
        <circle cx="44" cy="12" r="3" fill="#B7410E"/>
        <rect x="24" y="34" width="16" height="8" rx="1" fill="#DAA520" opacity="0.6"/>
    </svg>
    ''',
    'microwave': '''
    <svg viewBox="0 0 64 64" class="appliance-icon">
        <rect x="4" y="12" width="56" height="40" rx="4" fill="#F5F2EB" stroke="#4A4A4A" stroke-width="2"/>
        <rect x="10" y="18" width="34" height="28" rx="2" fill="#2D2D2D" opacity="0.8"/>
        <rect x="48" y="20" width="8" height="4" rx="1" fill="#6B8E23"/>
        <rect x="48" y="28" width="8" height="4" rx="1" fill="#DAA520"/>
        <rect x="48" y="36" width="8" height="4" rx="1" fill="#CC5500"/>
        <circle cx="52" cy="46" r="3" fill="#4A4A4A"/>
    </svg>
    '''
}


def render_appliance_strip():
    """Render a decorative strip of appliance icons"""
    icons_html = ''.join([APPLIANCES[a] for a in ['washer', 'dryer', 'fridge', 'dishwasher', 'oven', 'microwave']])
    st.markdown(f'''
    <div class="appliance-strip">
        {icons_html}
    </div>
    ''', unsafe_allow_html=True)


def render_appliance_icon(appliance: str, size: int = 48):
    """Render a single appliance icon"""
    if appliance in APPLIANCES:
        st.markdown(f'''
        <div style="width: {size}px; height: {size}px;">
            {APPLIANCES[appliance]}
        </div>
        ''', unsafe_allow_html=True)


def render_header_with_icons():
    """Render the header with appliance icons flanking the title"""
    icons_left = APPLIANCES['washer'] + APPLIANCES['fridge'] + APPLIANCES['oven']
    icons_right = APPLIANCES['dryer'] + APPLIANCES['dishwasher'] + APPLIANCES['microwave']
    
    st.markdown(f'''
    <div class="header-with-icons">
        <div class="header-icons left">{icons_left}</div>
        <div class="header-content">
            <h1 class="title">The Break-down Breakdown</h1>
            <p class="tagline">The breakdown on the stuff that breaks down.</p>
        </div>
        <div class="header-icons right">{icons_right}</div>
    </div>
    ''', unsafe_allow_html=True)

