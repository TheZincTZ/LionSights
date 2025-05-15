import folium
from geopy.geocoders import Nominatim
import requests
from PIL import Image
from io import BytesIO
import streamlit as st
import json
import os
from security import SecurityManager
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LocationData:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="lionsights")
        self.security = SecurityManager()
        self.load_location_data()
    
    def load_location_data(self):
        """Load location data from JSON file"""
        try:
            with open('data/locations.json', 'r', encoding='utf-8') as f:
                self.locations = json.load(f)
        except FileNotFoundError:
            self.locations = {}
            os.makedirs('data', exist_ok=True)
            with open('data/locations.json', 'w', encoding='utf-8') as f:
                json.dump(self.locations, f, indent=4)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in locations.json")
            self.locations = {}
        except Exception as e:
            logger.error(f"Error loading location data: {str(e)}")
            self.locations = {}

    def get_location_coordinates(self, location_name):
        """Get coordinates for a location"""
        if not self.security.validate_location_name(location_name):
            logger.warning(f"Invalid location name format: {location_name}")
            return None

        try:
            location = self.geolocator.geocode(location_name + ", Singapore")
            if location:
                return location.latitude, location.longitude
            return None
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            return None

    def create_map(self, location_name):
        """Create an interactive map for a location"""
        if not self.security.validate_location_name(location_name):
            return None

        coords = self.get_location_coordinates(location_name)
        if not coords:
            return None
        
        try:
            # Create a map centered on the location
            m = folium.Map(location=coords, zoom_start=15)
            
            # Add a marker for the location
            folium.Marker(
                coords,
                popup=self.security.sanitize_input(location_name),
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            return m
        except Exception as e:
            logger.error(f"Error creating map: {str(e)}")
            return None

    def get_location_images(self, location_name):
        """Get images for a location"""
        if not self.security.validate_location_name(location_name):
            return []

        if location_name in self.locations:
            images = self.locations[location_name].get('images', [])
            # Validate all image URLs
            return [img for img in images if self.security.validate_image_url(img)]
        return []

    def get_current_events(self, location_name):
        """Get current events and deals for a location"""
        if not self.security.validate_location_name(location_name):
            return []

        if location_name in self.locations:
            events = self.locations[location_name].get('events', [])
            # Sanitize event data
            return [{
                'title': self.security.sanitize_input(event.get('title', '')),
                'description': self.security.sanitize_input(event.get('description', '')),
                'valid_until': event.get('valid_until', '')
            } for event in events]
        return []

    def display_location_info(self, location_name):
        """Display comprehensive location information"""
        if not self.security.validate_location_name(location_name):
            st.error("Invalid location name format")
            return

        if location_name not in self.locations:
            st.warning("Location information not available.")
            return
        
        location_data = self.locations[location_name]
        
        # Create columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display map
            map_obj = self.create_map(location_name)
            if map_obj:
                st.components.v1.html(map_obj._repr_html_(), height=400)
            
            # Display images
            images = self.get_location_images(location_name)
            if images:
                st.subheader("Gallery")
                for img_url in images[:3]:  # Show first 3 images
                    try:
                        response = requests.get(img_url, timeout=5)  # Add timeout
                        response.raise_for_status()  # Raise exception for bad status codes
                        img = Image.open(BytesIO(response.content))
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        logger.error(f"Error loading image {img_url}: {str(e)}")
        
        with col2:
            # Display location details
            st.subheader("Location Details")
            st.write(self.security.secure_display(location_data.get('description', 'No description available.')))
            
            # Display current events and deals
            events = self.get_current_events(location_name)
            if events:
                st.subheader("Current Events & Deals")
                for event in events:
                    st.write(f"**{event['title']}**")
                    st.write(event['description'])
                    if 'valid_until' in event:
                        st.write(f"Valid until: {event['valid_until']}")
                    st.write("---") 