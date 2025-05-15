# LionSights: Your Ultimate Singapore Tourism Companion

Welcome to **LionSights**, an intelligent chatbot designed to enhance your travel experience in Singapore! Whether you're a first-time visitor or a seasoned explorer, LionSights is here to provide personalized recommendations for attractions, dining, activities, and hidden gems around the Lion City.

## Features
- **Personalized Recommendations**: Get tailored suggestions based on your interests and preferences.
- **Local Insights**: Discover off-the-beaten-path locations and local favorites.
- **Transportation Guidance**: Receive detailed information on how to reach your destination, including:
  - **Modes of Transport**: Options such as MRT, buses, taxis, and walking routes.
  - **Travel Times**: Estimated duration for each mode of transport.
- **Interactive Conversations**: Engage in natural language conversations for a seamless experience.
- **Up-to-Date Information**: Stay informed with the latest events, promotions, and travel tips.
- **User-Friendly Interface**: Easy to use, making your travel planning a breeze.
- **Visual Experience**: 
  - **Interactive Maps**: View locations on an interactive map with precise coordinates.
  - **Image Gallery**: Browse through high-quality images of attractions.
  - **Current Events**: Stay updated with ongoing events and special deals.
- **Location Intelligence**:
  - **Detailed Descriptions**: Get comprehensive information about each location.
  - **Current Events & Deals**: View active promotions and special events.
  - **Visual Navigation**: Interactive maps to help you find your way.
- **Review Integration**:
  - **Recent Reviews**: Access the latest reviews from TripAdvisor.
  - **Event Updates**: Get current 2025 events from TimeOut Singapore.
  - **Rating Information**: View overall ratings and detailed reviews.

## Getting Started
To get started with LionSights, simply clone this repository and follow the setup instructions in the [Installation](#installation) section.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/lionsights.git
cd lionsights
```

2. Create and activate a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. Run the application:
```bash
streamlit run app.py
```

## Security Features
LionSights implements several security measures to ensure a safe and reliable experience:
- **Input Validation**: All user inputs are validated and sanitized
- **Rate Limiting**: Prevents abuse by limiting request frequency
- **Secure Logging**: Comprehensive logging system for monitoring and debugging
- **Error Handling**: Robust error handling and user-friendly error messages
- **Dependency Security**: Pinned package versions for stability

## Contributing
We welcome contributions! Please check out our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
If you encounter any issues or have questions, please:
1. Check the [Issues](https://github.com/yourusername/lionsights/issues) page
2. Create a new issue if your problem hasn't been reported
3. Join our [Discord community](https://discord.gg/lionsights) for real-time support

Join us on this exciting journey to explore the wonders of Singapore with LionSights!
