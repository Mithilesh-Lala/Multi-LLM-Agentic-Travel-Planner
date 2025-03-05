import streamlit as st
import datetime
import os
from main import TravelPlanner

# Set page configuration
st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .agent-card {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #3b82f6;
    }
    .summary-card {
        background-color: #f0fff4;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Title and header
def render_header():
    """Render the app header and title"""
    st.title("🌎 AI Travel Planner")
    st.markdown("Let our AI agents help you plan your perfect trip!")

# Sidebar configuration
def render_sidebar():
    """Render the sidebar with configuration options and help text"""
    with st.sidebar:
        st.header("Configuration")
        
        model_type = st.radio(
            "Select AI Model",
            options=["Claude (Anthropic)", "GPT-4o (OpenAI)", "Gemini 1.5 (Google)"],
            index=0
        )
        
        # Map the selection to internal model type
        model_type_map = {
            "Claude (Anthropic)": "claude",
            "GPT-4o (OpenAI)": "openai",
            "Gemini 1.5 (Google)": "gemini"
        }
        
        # Display appropriate key input field
        if model_type == "Claude (Anthropic)":
            api_key = st.text_input("Enter Anthropic API Key", type="password")
            api_info = "You'll need an Anthropic API key with access to Claude 3.7 Sonnet"
        elif model_type == "GPT-4o (OpenAI)":
            api_key = st.text_input("Enter OpenAI API Key", type="password")
            api_info = "You'll need an OpenAI API key with access to GPT-4o"
        else:  # Gemini
            api_key = st.text_input("Enter Google AI API Key", type="password")
            api_info = "You'll need a Google AI API key with access to Gemini 1.5"
            
        st.info(api_info)
        
        st.markdown("---")
        st.markdown("### How it works")
        st.markdown("""
        This app uses multiple AI agents to plan your trip:
        1. **Flight Finder** searches for flights
        2. **Hotel Explorer** finds accommodations
        3. **Attraction Scout** discovers points of interest
        4. **Trip Summarizer** combines all information into a cohesive plan
        """)
        
        return api_key, model_type_map[model_type]

# Trip details form
def render_trip_form():
    """Render the form for trip details input"""
    with st.form("trip_details_form"):
        st.header("Enter Your Trip Details")
        col1, col2 = st.columns(2)
        
        with col1:
            origin = st.text_input("Origin City", "New York")
            destination = st.text_input("Destination City", "Tokyo")
            
        with col2:
            today = datetime.date.today()
            start_date = st.date_input("Departure Date", today + datetime.timedelta(days=30))
            end_date = st.date_input("Return Date", today + datetime.timedelta(days=37))
        
        trip_length = (end_date - start_date).days
        st.write(f"Trip Duration: {trip_length} days")
        
        col1, col2 = st.columns(2)
        with col1:
            budget = st.selectbox(
                "Budget Level",
                options=["Budget", "Moderate", "Luxury"],
                index=1
            )
        
        with col2:
            travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=2)
        
        interests = st.multiselect(
            "Interests",
            options=["History & Culture", "Nature & Outdoors", "Food & Cuisine", "Shopping", "Art & Museums", "Relaxation", "Adventure"],
            default=["History & Culture", "Food & Cuisine"]
        )
        
        submitted = st.form_submit_button("Plan My Trip")
        
        if submitted:
            return {
                'origin': origin,
                'destination': destination,
                'start_date': start_date,
                'end_date': end_date,
                'budget': budget,
                'travelers': travelers,
                'interests': interests,
                'submitted': True
            }
        return {'submitted': False}

# Display flight information
def display_flight_info(flight_result, flight_error):
    """Display flight information tab"""
    st.markdown(f"<div class='agent-card'><h3>🛫 Flight Finder</h3>", unsafe_allow_html=True)
    if flight_error:
        st.error(f"Error: {flight_error}")
    else:
        st.markdown(flight_result)
    st.markdown("</div>", unsafe_allow_html=True)

# Display hotel information
def display_hotel_info(hotel_result, hotel_error):
    """Display hotel information tab"""
    st.markdown(f"<div class='agent-card'><h3>🏨 Hotel Explorer</h3>", unsafe_allow_html=True)
    if hotel_error:
        st.error(f"Error: {hotel_error}")
    else:
        st.markdown(hotel_result)
    st.markdown("</div>", unsafe_allow_html=True)

# Display attraction information
def display_attraction_info(attraction_result, attraction_error):
    """Display attraction information tab"""
    st.markdown(f"<div class='agent-card'><h3>🏛️ Attraction Scout</h3>", unsafe_allow_html=True)
    if attraction_error:
        st.error(f"Error: {attraction_error}")
    else:
        st.markdown(attraction_result)
    st.markdown("</div>", unsafe_allow_html=True)

# Display trip summary
def display_trip_summary(summary_result, summary_error):
    """Display trip summary tab"""
    st.markdown(f"<div class='summary-card'><h3>📝 Trip Summarizer</h3>", unsafe_allow_html=True)
    if summary_error:
        st.error(f"Error: {summary_error}")
    else:
        st.markdown(summary_result)
    st.markdown("</div>", unsafe_allow_html=True)

# Display example content when app first loads
def display_example_content():
    """Display example content when app first loads"""
    st.info("Fill in your trip details and click 'Plan My Trip' to get started!")
    
    st.markdown("### Sample Trip Plan")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### Flight Options")
        st.markdown("• Multiple airlines with various departure times\n• Direct and connecting flight options\n• Price ranges for economy and business class")
    with col2:
        st.markdown("#### Hotel Recommendations")
        st.markdown("• Options for your chosen budget level\n• Best neighborhoods to stay in\n• Amenities and nearby attractions")
    with col3:
        st.markdown("#### Must-See Attractions")
        st.markdown("• Top-rated sights and experiences\n• Hidden gems and local favorites\n• Activities matched to your interests")

# Process trip planning
def process_trip_planning(api_key, model_type, trip_details):
    """Process trip planning with all agents"""
    if not api_key:
        st.error("Please enter an API key in the sidebar")
        return
    
    try:
        # Initialize the travel planner with the selected model type
        planner = TravelPlanner(api_key, model_type)
        
        # Show progress indicators
        progress_container = st.empty()
        progress_container.info("Planning your trip... This may take a minute or two.")
        
        # Generate the trip plan
        results = planner.generate_trip_plan(trip_details)
        
        # Clear progress indicator
        progress_container.empty()
        
        # Show results in tabs
        st.header("Your Trip Plan")
        tabs = st.tabs(["Flights", "Hotels", "Attractions", "Complete Trip Plan"])
        
        with tabs[0]:
            display_flight_info(results['flight_result'], results['errors']['flight_error'])
        
        with tabs[1]:
            display_hotel_info(results['hotel_result'], results['errors']['hotel_error'])
        
        with tabs[2]:
            display_attraction_info(results['attraction_result'], results['errors']['attraction_error'])
        
        with tabs[3]:
            display_trip_summary(results['summary_result'], results['errors']['summary_error'])
        
        # Add download button for the trip plan
        st.download_button(
            label="Download Trip Plan",
            data=results['trip_plan_text'],
            file_name=f"trip_plan_{trip_details['destination']}_{trip_details['start_date'].strftime('%Y-%m-%d')}.md",
            mime="text/markdown"
        )
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Main app function
def main():
    """Main app function"""
    render_header()
    api_key, model_type = render_sidebar()
    trip_details = render_trip_form()
    
    if trip_details['submitted']:
        process_trip_planning(api_key, model_type, trip_details)
    else:
        display_example_content()

if __name__ == "__main__":
    main()