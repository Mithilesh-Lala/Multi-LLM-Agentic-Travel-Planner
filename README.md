# Multi-LLM Agentic Travel Planner

An agentic application that leverages multiple Large Language Model providers (OpenAI, Anthropic, and Google) to help plan trips by coordinating specialized AI agents.

## 🌟 Features

- **Multiple LLM Support**: Choose between Claude 3.7 (Anthropic), GPT-4o (OpenAI), or Gemini 1.5 (Google)
- **Flight Finder Agent**: Searches for flights between origin and destination for specific dates
- **Hotel Explorer Agent**: Finds suitable accommodations at the destination within budget
- **Attraction Scout Agent**: Discovers interesting places and activities at the destination
- **Trip Summarizer Agent**: Creates a comprehensive trip plan by combining information from all agents
- **Downloadable Itineraries**: Get your complete trip plan as a markdown file

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- API keys for at least one of the supported LLM providers:
  - Anthropic API key (for Claude)
  - OpenAI API key (for GPT-4o)
  - Google AI API key (for Gemini 1.5)

### Installation

1. Clone this repository:
   ```bash
   https://github.com/Mithilesh-Lala/Multi-LLM-Agentic-Travel-Planner.git
   cd to project directory
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## 💻 Usage

1. Select your preferred LLM provider in the sidebar
2. Enter the appropriate API key
3. Fill in your trip details:
   - Origin and destination cities
   - Departure and return dates
   - Budget level
   - Number of travelers
   - Interests
4. Click "Plan My Trip"
5. View the results in each tab:
   - Flights
   - Hotels
   - Attractions
   - Complete Trip Plan
6. Download your complete trip plan as a markdown file

## 🏗️ Architecture

The application is built using a modular architecture:

- **app.py**: Streamlit user interface
- **main.py**: Core application logic and agent coordination

### Agent System

The application uses four specialized AI agents:

1. **Flight Finder Agent**: Focused on transportation options
2. **Hotel Explorer Agent**: Specialized in finding accommodations
3. **Attraction Scout Agent**: Expert in points of interest and activities
4. **Trip Summarizer Agent**: Combines information into a cohesive plan

Each agent has a specialized system prompt that guides its responses, and all agents use the same selected LLM provider for consistency.

## 🛠️ Customization

You can extend this application in several ways:

- Add more specialized agents (e.g., for car rentals, dining recommendations)
- Customize agent prompts in the `main.py` file
- Enhance the UI with additional filters or visualization options
- Integrate with actual travel APIs for real-time data (flight APIs, hotel booking systems)

## 📋 Requirements

- streamlit==1.28.0
- anthropic==0.8.1
- openai==1.10.0
- google-generativeai==0.3.1
- python-dotenv==1.0.0

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.


## 🙏 Acknowledgements

- This project uses the [Anthropic Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api)
- [OpenAI API](https://platform.openai.com/docs/api-reference) for GPT-4o integration
- [Google Generative AI API](https://ai.google.dev/docs) for Gemini 1.5 integration
- [Streamlit](https://streamlit.io/) for the user interface
