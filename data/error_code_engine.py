"""
Error Code Engine
Evaluates current conditions and triggers diagnostic codes
"""
from typing import List, Dict, Callable


# Error code definitions
ERROR_CODES = {
    "E7": {
        "name": "TECH_SHORTAGE_DETECTED",
        "condition": lambda d: d.get('hiring_difficulty_avg', 0) >= 3.5,
        "message": "Technician supply is constrained. Finding qualified candidates is harder than usual.",
        "severity": "warning",
        "recommendation": "Consider apprenticeship programs or reaching out to trade schools."
    },
    "F3": {
        "name": "PARTS_LEAD_TIME_EXTENDED",
        "condition": lambda d: d.get('parts_lead_time_avg', 0) >= 10,
        "message": "Parts lead times are extended beyond normal levels.",
        "severity": "warning",
        "recommendation": "Stock up on common failure parts and expand supplier relationships."
    },
    "C1": {
        "name": "CONSUMER_DEMAND_STRONG",
        "condition": lambda d: d.get('call_volume_sentiment_avg', 0) >= 3.5,
        "message": "Consumer demand for appliance repair is healthy.",
        "severity": "good",
        "recommendation": "Good time to invest in capacity and marketing."
    },
    "C2": {
        "name": "CONSUMER_DEMAND_WEAK",
        "condition": lambda d: d.get('call_volume_sentiment_avg', 5) <= 2.0,
        "message": "Consumer demand is below normal levels.",
        "severity": "warning",
        "recommendation": "Focus on marketing and consider diversifying services."
    },
    "E2": {
        "name": "TARIFF_PRESSURE_ACTIVE",
        "condition": lambda d: d.get('tariff_alert_active', False),
        "message": "Tariff-related cost pressure is affecting parts prices.",
        "severity": "warning",
        "recommendation": "Review pricing and consider domestic parts alternatives."
    },
    "H1": {
        "name": "HOUSING_TURNOVER_LOW",
        "condition": lambda d: d.get('existing_home_sales_change', 0) <= 0.02,
        "message": "Low housing turnover means homeowners are staying put and maintaining appliances.",
        "severity": "good",
        "recommendation": "Stable customer base - focus on retention and service agreements."
    },
    "H2": {
        "name": "HOUSING_TURNOVER_HIGH",
        "condition": lambda d: d.get('existing_home_sales_change', 0) >= 0.10,
        "message": "High housing turnover may mean more appliance replacements over repairs.",
        "severity": "warning",
        "recommendation": "Target new homeowners who inherit older appliances."
    },
    "R1": {
        "name": "RIGHT_TO_REPAIR_EXPANDING",
        "condition": lambda d: d.get('r2r_laws_passed_this_year', 0) >= 1,
        "message": "Right to Repair legislation is expanding access to parts and manuals.",
        "severity": "good",
        "recommendation": "Take advantage of improved parts availability."
    },
    "P1": {
        "name": "PARTS_PRICES_RISING",
        "condition": lambda d: d.get('appliance_cpi_change', 0) >= 0.05,
        "message": "New appliance prices are rising, making repairs more attractive to consumers.",
        "severity": "good",
        "recommendation": "Emphasize repair cost savings vs replacement in marketing."
    },
    "B1": {
        "name": "BUSINESS_SENTIMENT_STRONG",
        "condition": lambda d: d.get('business_sentiment_avg', 0) >= 4.0,
        "message": "Fellow servicers report strong business conditions.",
        "severity": "good",
        "recommendation": "Conditions are favorable - consider expansion."
    },
    "B2": {
        "name": "BUSINESS_SENTIMENT_WEAK",
        "condition": lambda d: d.get('business_sentiment_avg', 5) <= 2.0,
        "message": "Fellow servicers report challenging business conditions.",
        "severity": "warning",
        "recommendation": "Focus on efficiency and cash reserves."
    },
}


def evaluate_error_codes(data: Dict) -> List[Dict]:
    """
    Evaluate all error codes against current data.
    
    Args:
        data: Dictionary containing current metric values
    
    Returns:
        List of triggered error code dictionaries
    """
    triggered = []
    
    for code_id, code_def in ERROR_CODES.items():
        try:
            if code_def['condition'](data):
                triggered.append({
                    'code': code_id,
                    'name': code_def['name'],
                    'message': code_def['message'],
                    'severity': code_def['severity'],
                    'recommendation': code_def.get('recommendation', '')
                })
        except Exception:
            # Skip codes that error on evaluation
            pass
    
    return triggered


def get_active_error_codes() -> List[Dict]:
    """
    Get currently active error codes based on latest data.
    
    Returns:
        List of active error code dictionaries
    """
    # TODO: Replace with actual data fetching
    # Mock data for development
    mock_data = {
        'hiring_difficulty_avg': 3.8,
        'parts_lead_time_avg': 8.5,
        'call_volume_sentiment_avg': 3.4,
        'tariff_alert_active': True,
        'existing_home_sales_change': 0.01,
        'r2r_laws_passed_this_year': 2,
        'appliance_cpi_change': 0.03,
        'business_sentiment_avg': 3.2,
    }
    
    return evaluate_error_codes(mock_data)

