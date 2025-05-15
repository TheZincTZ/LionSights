import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging
import config

logger = logging.getLogger(__name__)

class ReviewsData:
    def __init__(self):
        self.current_year = datetime.now().year
        
    def get_place_reviews(self, place_name):
        """
        Get reviews from TripAdvisor using web scraping
        """
        try:
            # Format place name for URL
            formatted_name = place_name.lower().replace(' ', '-')
            url = f"https://www.tripadvisor.com/Search?q={formatted_name}&searchType=attraction"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract reviews (this is a simplified example - actual selectors would need to be updated)
            reviews = []
            review_elements = soup.find_all('div', class_='review-container')
            
            for review in review_elements[:5]:  # Get top 5 reviews
                try:
                    rating = review.find('span', class_='ui_bubble_rating')['class'][1].split('_')[1]
                    text = review.find('p', class_='partial_entry').text.strip()
                    date = review.find('span', class_='ratingDate')['title']
                    
                    reviews.append({
                        'rating': float(rating) / 10,
                        'text': text,
                        'date': date
                    })
                except:
                    continue
            
            return {
                'name': place_name,
                'rating': sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0,
                'total_ratings': len(reviews),
                'reviews': reviews
            }
            
        except Exception as e:
            logger.error(f"Error fetching reviews: {str(e)}")
            return None
            
    def get_current_events(self, place_name):
        """
        Get current events and activities for 2025 from local event websites
        """
        try:
            # Example: Search for events on TimeOut Singapore
            url = f"https://www.timeout.com/singapore/things-to-do/events-in-singapore"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            current_events = []
            event_elements = soup.find_all('div', class_='card-content')
            
            for event in event_elements[:5]:  # Get top 5 events
                try:
                    name = event.find('h3').text.strip()
                    if '2025' in name:
                        current_events.append({
                            'name': name,
                            'description': event.find('p').text.strip(),
                            'date': event.find('time').text.strip()
                        })
                except:
                    continue
                    
            return current_events
            
        except Exception as e:
            logger.error(f"Error fetching current events: {str(e)}")
            return None
            
    def format_reviews_response(self, place_name, reviews, current_events):
        """
        Format all review data into a comprehensive response
        """
        response = f"Current Information for {place_name} (2025):\n\n"
        
        if reviews:
            response += "Recent Reviews:\n"
            response += f"Overall Rating: {reviews['rating']:.1f} ({reviews['total_ratings']} ratings)\n\n"
            
            for review in reviews['reviews']:
                response += f"Rating: {review['rating']} stars\n"
                response += f"Review: {review['text']}\n"
                response += f"Date: {review['date']}\n\n"
                
        if current_events:
            response += "\nCurrent Events (2025):\n"
            for event in current_events:
                response += f"Event: {event['name']}\n"
                response += f"Description: {event['description']}\n"
                response += f"Date: {event['date']}\n\n"
                
        return response 