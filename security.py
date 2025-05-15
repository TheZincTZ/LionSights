import time
import html
import bleach
from typing import Optional
import streamlit as st
import re
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self):
        self.rate_limit_window = 2  # seconds
        self.max_requests_per_window = 5
        self.max_input_length = 1000  # characters
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize security-related session state variables"""
        if 'last_request' not in st.session_state:
            st.session_state.last_request = 0
        if 'request_count' not in st.session_state:
            st.session_state.request_count = 0
        if 'request_timestamps' not in st.session_state:
            st.session_state.request_timestamps = []

    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent XSS and injection attacks"""
        if not user_input:
            return ""
        
        # Remove any HTML tags
        cleaned = bleach.clean(user_input, strip=True)
        
        # Escape HTML entities
        cleaned = html.escape(cleaned)
        
        # Remove any potential script tags
        cleaned = re.sub(r'<script.*?>.*?</script>', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        
        return cleaned

    def check_rate_limit(self) -> bool:
        """Check if the current request exceeds rate limits"""
        current_time = time.time()
        
        # Remove timestamps older than the window
        st.session_state.request_timestamps = [
            ts for ts in st.session_state.request_timestamps 
            if current_time - ts < self.rate_limit_window
        ]
        
        # Check if we've exceeded the rate limit
        if len(st.session_state.request_timestamps) >= self.max_requests_per_window:
            return False
        
        # Add current timestamp
        st.session_state.request_timestamps.append(current_time)
        return True

    def validate_input_length(self, user_input: str) -> bool:
        """Validate that input length is within acceptable limits"""
        return len(user_input) <= self.max_input_length

    def secure_display(self, content: str) -> str:
        """Safely prepare content for display"""
        return self.sanitize_input(content)

    def log_security_event(self, event_type: str, details: str):
        """Log security-related events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {event_type}: {details}"
        
        # In a production environment, you would want to log this to a secure logging system
        print(log_entry)  # Replace with proper logging

    def validate_location_name(self, location_name: str) -> bool:
        """Validate location name format"""
        # Only allow alphanumeric characters, spaces, and basic punctuation
        return bool(re.match(r'^[a-zA-Z0-9\s\-\.,]+$', location_name))

    def validate_image_url(self, url: str) -> bool:
        """Validate image URL format"""
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url)) 