from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import config

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
        
    def get_response(self, user_input):
        """
        Get a response from the chatbot based on user input
        """
        try:
            # Create messages for the conversation
            messages = [
                SystemMessage(content=config.SYSTEM_PROMPT),
                HumanMessage(content=user_input)
            ]
            
            # Get response from the model
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."

    def clear_memory(self):
        """
        Clear the conversation memory
        """
        self.memory.clear() 