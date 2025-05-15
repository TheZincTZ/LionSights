import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4-turbo-preview"  # Using the latest GPT-4 model

# Google Maps Configuration
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

# Chatbot Configuration
SYSTEM_PROMPT = """You are LionSights, an intelligent travel assistant for Singapore. 
Your role is to provide accurate, up-to-date information about attractions, dining, activities, and hidden gems in Singapore.
Always include current information from 2025 and recent reviews when available.
Be friendly, helpful, and provide detailed responses that help tourists make informed decisions.
Include practical information like opening hours, prices, and transportation options when relevant.
If you're unsure about any information, be honest about it and suggest alternative sources."""

# Streamlit Configuration
STREAMLIT_TITLE = "LionSights - Your Singapore Tourism Companion"
STREAMLIT_DESCRIPTION = "Get personalized recommendations for your Singapore adventure!"

# Security Configuration
MAX_INPUT_LENGTH = 1000
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW = 2  # seconds 