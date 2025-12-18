"""
FRED API Client
Fetches economic indicators from Federal Reserve Economic Data
"""
import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta

def get_secret(key: str) -> Optional[str]:
    """Get secret from Streamlit secrets or env vars"""
    try:
        import streamlit as st
        return st.secrets.get(key)
    except:
        pass
    return os.getenv(key)

# FRED API series IDs
FRED_SERIES = {
    'consumer_confidence': 'UMCSENT',      # U of Michigan Consumer Sentiment
    'existing_home_sales': 'EXHOSLUSM495S', # Existing Home Sales
    'mortgage_rate': 'MORTGAGE30US',        # 30-Year Mortgage Rate
    'appliance_cpi': 'CUSR0000SEHK',        # Major Appliances CPI
    'durable_goods_orders': 'DGORDER',      # Durable Goods Orders
    'housing_inventory': 'ACTLISCOUUS',     # Active Listings Count
}


class FREDClient:
    """Client for fetching data from FRED API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_secret('FRED_API_KEY')
        self.base_url = 'https://api.stlouisfed.org/fred'
        self._cache: Dict = {}
        self._cache_expiry: Dict[str, datetime] = {}
    
    def _is_cache_valid(self, series_id: str, max_age_hours: int = 24) -> bool:
        """Check if cached data is still valid"""
        if series_id not in self._cache_expiry:
            return False
        return datetime.now() < self._cache_expiry[series_id]
    
    def get_series_latest(self, series_id: str) -> Optional[float]:
        """
        Get the latest value for a FRED series.
        
        Args:
            series_id: FRED series identifier
        
        Returns:
            Latest value or None if unavailable
        """
        if self._is_cache_valid(series_id):
            return self._cache.get(series_id)
        
        if not self.api_key:
            # Return mock data if no API key
            return self._get_mock_value(series_id)
        
        try:
            import requests
            
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json',
                'sort_order': 'desc',
                'limit': 1,
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('observations'):
                value = float(data['observations'][0]['value'])
                
                # Cache the result
                self._cache[series_id] = value
                self._cache_expiry[series_id] = datetime.now() + timedelta(hours=24)
                
                return value
        except Exception as e:
            print(f"Error fetching FRED series {series_id}: {e}")
        
        return self._get_mock_value(series_id)
    
    def get_series_history(
        self, 
        series_id: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict]:
        """
        Get historical values for a FRED series.
        
        Args:
            series_id: FRED series identifier
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
        
        Returns:
            List of dicts with 'date' and 'value' keys
        """
        if not self.api_key:
            return []
        
        try:
            import requests
            
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': series_id,
                'api_key': self.api_key,
                'file_type': 'json',
            }
            
            if start_date:
                params['observation_start'] = start_date
            if end_date:
                params['observation_end'] = end_date
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return [
                {'date': obs['date'], 'value': float(obs['value'])}
                for obs in data.get('observations', [])
                if obs['value'] != '.'
            ]
        except Exception as e:
            print(f"Error fetching FRED history {series_id}: {e}")
        
        return []
    
    def _get_mock_value(self, series_id: str) -> float:
        """Return mock values for development"""
        mock_values = {
            'UMCSENT': 68.5,
            'EXHOSLUSM495S': 4100,
            'MORTGAGE30US': 6.8,
            'CUSR0000SEHK': 108.5,
            'DGORDER': 285000,
            'ACTLISCOUUS': 750000,
        }
        return mock_values.get(series_id, 50.0)
    
    def get_all_indicators(self) -> Dict[str, float]:
        """
        Fetch all configured FRED indicators.
        
        Returns:
            Dict mapping indicator names to values
        """
        results = {}
        for name, series_id in FRED_SERIES.items():
            value = self.get_series_latest(series_id)
            if value is not None:
                results[name] = value
        return results


# Singleton instance
_client: Optional[FREDClient] = None


def get_fred_client() -> FREDClient:
    """Get or create FRED client instance"""
    global _client
    if _client is None:
        _client = FREDClient()
    return _client

