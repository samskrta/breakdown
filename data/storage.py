"""
Data Storage Layer
Handles persistence of field reports and cached data
Supports both local JSON (dev) and Supabase (production)
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Try Streamlit secrets first (for Streamlit Cloud), then env vars
def get_secret(key: str) -> Optional[str]:
    try:
        import streamlit as st
        return st.secrets.get(key)
    except:
        pass
    return os.getenv(key)

# Storage mode
USE_SUPABASE = bool(get_secret('SUPABASE_URL'))

# Local storage paths
DATA_DIR = Path(__file__).parent / "local_data"
REPORTS_FILE = DATA_DIR / "field_reports.json"
CACHE_FILE = DATA_DIR / "indicator_cache.json"


def _ensure_local_storage():
    """Create local storage directory and files if needed"""
    DATA_DIR.mkdir(exist_ok=True)
    if not REPORTS_FILE.exists():
        REPORTS_FILE.write_text("[]")
    if not CACHE_FILE.exists():
        CACHE_FILE.write_text("{}")


class LocalStorage:
    """JSON file-based storage for development"""
    
    def __init__(self):
        _ensure_local_storage()
    
    def save_field_report(self, report: Dict) -> bool:
        """Save a field report submission"""
        try:
            reports = json.loads(REPORTS_FILE.read_text())
            reports.append(report)
            REPORTS_FILE.write_text(json.dumps(reports, indent=2))
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    def get_field_reports(
        self, 
        month: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Dict]:
        """Get field reports, optionally filtered"""
        try:
            reports = json.loads(REPORTS_FILE.read_text())
            
            if month:
                reports = [r for r in reports if r.get('timestamp', '').startswith(month)]
            if region:
                reports = [r for r in reports if r.get('region') == region]
            
            return reports
        except Exception:
            return []
    
    def get_report_count(self, month: Optional[str] = None) -> int:
        """Get count of reports"""
        return len(self.get_field_reports(month=month))
    
    def get_aggregated_metrics(self, month: Optional[str] = None) -> Dict:
        """Get aggregated metrics from field reports"""
        reports = self.get_field_reports(month=month)
        
        if not reports:
            return {}
        
        # Calculate averages
        call_volumes = [r['call_volume'] for r in reports if 'call_volume' in r]
        lead_times = [r['parts_lead_time'] for r in reports if 'parts_lead_time' in r]
        sentiments = [r['business_sentiment'] for r in reports if 'business_sentiment' in r]
        difficulties = [
            r['hiring_difficulty'] for r in reports 
            if r.get('hiring_difficulty') is not None
        ]
        
        return {
            'call_volume_sentiment_avg': sum(call_volumes) / len(call_volumes) if call_volumes else 3.0,
            'parts_lead_time_avg': sum(lead_times) / len(lead_times) if lead_times else 7.0,
            'business_sentiment_avg': sum(sentiments) / len(sentiments) if sentiments else 3.0,
            'hiring_difficulty_avg': sum(difficulties) / len(difficulties) if difficulties else 3.0,
            'report_count': len(reports)
        }
    
    def cache_indicator(self, key: str, value: float, timestamp: str):
        """Cache an indicator value"""
        try:
            cache = json.loads(CACHE_FILE.read_text())
            cache[key] = {'value': value, 'timestamp': timestamp}
            CACHE_FILE.write_text(json.dumps(cache, indent=2))
        except Exception as e:
            print(f"Error caching indicator: {e}")
    
    def get_cached_indicator(self, key: str) -> Optional[Dict]:
        """Get a cached indicator value"""
        try:
            cache = json.loads(CACHE_FILE.read_text())
            return cache.get(key)
        except Exception:
            return None


class SupabaseStorage:
    """Supabase-based storage for production"""
    
    def __init__(self):
        try:
            from supabase import create_client
            self.client = create_client(
                get_secret('SUPABASE_URL'),
                get_secret('SUPABASE_KEY')
            )
        except Exception as e:
            print(f"Supabase init failed: {e}")
            self.client = None
    
    def save_field_report(self, report: Dict) -> bool:
        """Save a field report to Supabase"""
        if not self.client:
            return False
        
        try:
            self.client.table('field_reports').insert(report).execute()
            return True
        except Exception as e:
            print(f"Supabase save error: {e}")
            return False
    
    def get_field_reports(
        self, 
        month: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Dict]:
        """Get field reports from Supabase"""
        if not self.client:
            return []
        
        try:
            query = self.client.table('field_reports').select('*')
            
            if month:
                query = query.gte('timestamp', f'{month}-01').lt('timestamp', f'{month}-32')
            if region:
                query = query.eq('region', region)
            
            result = query.execute()
            return result.data or []
        except Exception as e:
            print(f"Supabase query error: {e}")
            return []
    
    def get_report_count(self, month: Optional[str] = None) -> int:
        """Get count of reports from Supabase"""
        if not self.client:
            return 0
        
        try:
            query = self.client.table('field_reports').select('id', count='exact')
            if month:
                query = query.gte('timestamp', f'{month}-01').lt('timestamp', f'{month}-32')
            result = query.execute()
            return result.count or 0
        except Exception:
            return 0
    
    def get_aggregated_metrics(self, month: Optional[str] = None) -> Dict:
        """Get aggregated metrics from Supabase"""
        # For now, fall back to fetching all and aggregating client-side
        # Could optimize with database aggregation functions
        reports = self.get_field_reports(month=month)
        
        if not reports:
            return {}
        
        call_volumes = [r['call_volume'] for r in reports if 'call_volume' in r]
        lead_times = [r['parts_lead_time'] for r in reports if 'parts_lead_time' in r]
        sentiments = [r['business_sentiment'] for r in reports if 'business_sentiment' in r]
        difficulties = [
            r['hiring_difficulty'] for r in reports 
            if r.get('hiring_difficulty') is not None
        ]
        
        return {
            'call_volume_sentiment_avg': sum(call_volumes) / len(call_volumes) if call_volumes else 3.0,
            'parts_lead_time_avg': sum(lead_times) / len(lead_times) if lead_times else 7.0,
            'business_sentiment_avg': sum(sentiments) / len(sentiments) if sentiments else 3.0,
            'hiring_difficulty_avg': sum(difficulties) / len(difficulties) if difficulties else 3.0,
            'report_count': len(reports)
        }


# Storage singleton
_storage = None


def get_storage():
    """Get the appropriate storage backend"""
    global _storage
    if _storage is None:
        if USE_SUPABASE:
            _storage = SupabaseStorage()
        else:
            _storage = LocalStorage()
    return _storage

