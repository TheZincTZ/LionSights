from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from location_data import LocationData
from security import SecurityManager
import config
import streamlit as st
import logging

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LionSightsChatbot:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=config.MODEL_NAME,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        self.location_data = LocationData()
        self.security = SecurityManager()
        
    def get_response(self, user_input):
        """
        Get a response from the chatbot based on user input
        """
        try:
            # Security checks
            if not self.security.check_rate_limit():
                logger.warning("Rate limit exceeded")
                return "Please wait a moment before sending another message."

            if not self.security.validate_input_length(user_input):
                logger.warning("Input length exceeded")
                return "Your message is too long. Please keep it under 1000 characters."

            # Sanitize input
            sanitized_input = self.security.sanitize_input(user_input)
            
            # Create messages for the conversation
            messages = [
                SystemMessage(content=config.SYSTEM_PROMPT),
                HumanMessage(content=sanitized_input)
            ]
            
            # Get response from the model
            response = self.llm.invoke(messages)
            
            # Check if the response mentions any known locations
            for location in self.location_data.locations.keys():
                if location.lower() in sanitized_input.lower():
                    # Display location information
                    self.location_data.display_location_info(location)
            
            # Log the interaction
            logger.info(f"User query: {sanitized_input[:100]}...")  # Log first 100 chars only
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error in chatbot response: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

    def clear_memory(self):
        """
        Clear the conversation memory
        """
        try:
            self.memory.clear()
            logger.info("Chat memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}") 