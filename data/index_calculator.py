"""
Breakdown Index Calculator
Composite score calculation from multiple data sources
"""
from typing import Dict, List
from datetime import datetime


# Weights for each component
WEIGHTS = {
    # Economic indicators (50%)
    'consumer_confidence': 0.10,
    'existing_home_sales': 0.15,
    'mortgage_rate': 0.10,
    'appliance_cpi': 0.15,
    
    # Industry indicators (25%)
    'appliance_shipments': 0.10,
    'tech_wage_growth': 0.05,
    'job_posting_volume': 0.05,
    'parts_availability': 0.05,
    
    # Field report data (25%)
    'call_volume_sentiment': 0.10,
    'parts_lead_time': 0.05,
    'hiring_difficulty': 0.05,
    'business_sentiment': 0.05,
}


def normalize(value: float, min_val: float, max_val: float, inverse: bool = False) -> float:
    """
    Normalize a value to 0-100 scale based on historical range.
    
    Args:
        value: Current value
        min_val: Historical minimum
        max_val: Historical maximum
        inverse: If True, lower values = higher score
    """
    if max_val == min_val:
        return 50.0
    
    normalized = (value - min_val) / (max_val - min_val) * 100
    normalized = max(0, min(100, normalized))  # Clamp to 0-100
    
    if inverse:
        normalized = 100 - normalized
    
    return normalized


def calculate_breakdown_index(data: Dict) -> float:
    """
    Calculate composite Breakdown Index score (0-100).
    Higher = better conditions for repair businesses.
    
    Args:
        data: Dictionary containing all indicator values
    
    Returns:
        Composite score 0-100
    """
    score = 0.0
    
    # Economic indicators (higher is generally good for repair)
    # Consumer Confidence: 50-120 historical range
    if 'consumer_confidence' in data:
        score += normalize(data['consumer_confidence'], 50, 120) * WEIGHTS['consumer_confidence']
    
    # Existing Home Sales: Low turnover = good for repair (inverse)
    # Range: 3M - 7M units annually
    if 'existing_home_sales' in data:
        score += normalize(data['existing_home_sales'], 3.0, 7.0, inverse=True) * WEIGHTS['existing_home_sales']
    
    # Mortgage Rate: High rates = people stay put = good (inverse for high = good)
    # Range: 2% - 8%
    if 'mortgage_rate' in data:
        # High rates keep people in homes = more repairs
        score += normalize(data['mortgage_rate'], 2.0, 8.0) * WEIGHTS['mortgage_rate']
    
    # Appliance CPI: Higher new prices = more repair demand
    # Range: 90 - 130 index
    if 'appliance_cpi' in data:
        score += normalize(data['appliance_cpi'], 90, 130) * WEIGHTS['appliance_cpi']
    
    # Industry indicators
    # Appliance Shipments: Low = more repair demand (inverse)
    if 'appliance_shipments' in data:
        score += normalize(data['appliance_shipments'], 5, 15, inverse=True) * WEIGHTS['appliance_shipments']
    
    # Tech Wage Growth: Lower growth = easier to hire (inverse)
    if 'tech_wage_growth' in data:
        score += normalize(data['tech_wage_growth'], 0, 10, inverse=True) * WEIGHTS['tech_wage_growth']
    
    # Job Posting Volume: More postings = tighter labor (inverse)
    if 'job_posting_volume' in data:
        score += normalize(data['job_posting_volume'], 0, 100, inverse=True) * WEIGHTS['job_posting_volume']
    
    # Parts Availability: 1-5 scale, higher = better
    if 'parts_availability' in data:
        score += normalize(data['parts_availability'], 1, 5) * WEIGHTS['parts_availability']
    
    # Field report data
    # Call Volume Sentiment: 1-5 scale, higher = better
    if 'call_volume_sentiment' in data:
        score += normalize(data['call_volume_sentiment'], 1, 5) * WEIGHTS['call_volume_sentiment']
    
    # Parts Lead Time: Lower = better (inverse)
    if 'parts_lead_time' in data:
        score += normalize(data['parts_lead_time'], 1, 30, inverse=True) * WEIGHTS['parts_lead_time']
    
    # Hiring Difficulty: Lower = better (inverse)
    if 'hiring_difficulty' in data:
        score += normalize(data['hiring_difficulty'], 1, 5, inverse=True) * WEIGHTS['hiring_difficulty']
    
    # Business Sentiment: 1-5 scale, higher = better
    if 'business_sentiment' in data:
        score += normalize(data['business_sentiment'], 1, 5) * WEIGHTS['business_sentiment']
    
    return round(score, 1)


def get_current_index() -> Dict:
    """
    Get the current Breakdown Index score and metadata.
    
    Returns:
        Dict with 'score', 'change', 'date', 'zone'
    """
    # TODO: Replace with actual data fetching
    # Mock data for development
    mock_data = {
        'consumer_confidence': 68.5,
        'existing_home_sales': 4.1,
        'mortgage_rate': 6.8,
        'appliance_cpi': 108.5,
        'appliance_shipments': 8.2,
        'tech_wage_growth': 4.5,
        'job_posting_volume': 62,
        'parts_availability': 3.2,
        'call_volume_sentiment': 3.4,
        'parts_lead_time': 8.5,
        'hiring_difficulty': 3.8,
        'business_sentiment': 3.2,
    }
    
    score = calculate_breakdown_index(mock_data)
    
    return {
        'score': score,
        'change': 2.3,  # Mock: up 2.3 from last month
        'date': datetime.now().strftime('%B %Y'),
        'zone': get_zone_name(score)
    }


def get_zone_name(score: float) -> str:
    """Get zone name from score"""
    if score >= 80:
        return "Gravy Train"
    elif score >= 60:
        return "Humming Along"
    elif score >= 40:
        return "Check Engine"
    elif score >= 20:
        return "Parts on Backorder"
    else:
        return "Total Breakdown"


def get_index_history() -> List[Dict]:
    """
    Get historical index scores for sparkline display.
    
    Returns:
        List of dicts with 'month' and 'score' keys
    """
    # TODO: Replace with actual historical data
    # Mock 12-month history
    return [
        {'month': 'Jan', 'score': 52},
        {'month': 'Feb', 'score': 54},
        {'month': 'Mar', 'score': 51},
        {'month': 'Apr', 'score': 55},
        {'month': 'May', 'score': 58},
        {'month': 'Jun', 'score': 56},
        {'month': 'Jul', 'score': 59},
        {'month': 'Aug', 'score': 61},
        {'month': 'Sep', 'score': 58},
        {'month': 'Oct', 'score': 55},
        {'month': 'Nov', 'score': 54},
        {'month': 'Dec', 'score': 56},
    ]

