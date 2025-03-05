import anthropic
import openai
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import datetime

class Agent:
    """Base class for all AI agents in the system"""
    def __init__(self, name: str, description: str, system_prompt: str):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.result = None
        self.loading = False
        self.error = None
    
    def run(self, client, user_prompt: str, model_type: str, model_name: str):
        """Run the agent with the given prompt using specified model type and name"""
        self.loading = True
        self.error = None
        
        try:
            if model_type == "claude":
                response = client.messages.create(
                    model=model_name,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                    max_tokens=2000,
                )
                self.result = response.content[0].text
                
            elif model_type == "openai":
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=2000,
                )
                self.result = response.choices[0].message.content
                
            elif model_type == "gemini":
                model = client.GenerativeModel(model_name)
                chat = model.start_chat(history=[])
                response = chat.send_message(
                    f"System instruction: {self.system_prompt}\n\nUser request: {user_prompt}"
                )
                self.result = response.text
                
            return self.result
            
        except Exception as e:
            self.error = str(e)
            return None
        finally:
            self.loading = False

# Define specialized agents
def create_flight_agent() -> Agent:
    """Create and return the Flight Finder agent"""
    return Agent(
        name="Flight Finder",
        description="Searches for available flights between your origin and destination",
        system_prompt="""You are an AI agent specializing in finding flight information. 
        
Your task is to provide realistic flight options between an origin and destination for specific dates.
Include details such as:
- Airline options
- Approximate flight times and durations
- Price ranges
- Direct vs connecting flights
- Best times to fly
- Any potential travel advisories

Format your response in a clear, easy-to-read manner with sections.
Base your information on general knowledge about typical flight routes, airlines that serve those routes, and approximate costs.
DO NOT make up specific flights with exact times and prices."""
    )

def create_hotel_agent() -> Agent:
    """Create and return the Hotel Explorer agent"""
    return Agent(
        name="Hotel Explorer",
        description="Finds suitable accommodations at your destination within budget",
        system_prompt="""You are an AI agent specializing in finding hotel and accommodation information.
        
Your task is to provide realistic hotel options at a given destination within a specified budget range.
Include details such as:
- Variety of hotel types (luxury, mid-range, budget)
- Approximate price ranges
- Popular neighborhoods or areas to stay
- Amenities typically available
- Pros and cons of different areas
- Any seasonal considerations

Format your response in a clear, easy-to-read manner with sections.
Base your information on general knowledge about typical accommodations in the area.
DO NOT make up specific hotel names, exact prices, or claim to know real-time availability."""
    )

def create_attraction_agent() -> Agent:
    """Create and return the Attraction Scout agent"""
    return Agent(
        name="Attraction Scout",
        description="Discovers interesting places and activities at your destination",
        system_prompt="""You are an AI agent specializing in tourist attractions and points of interest.
        
Your task is to provide information about interesting places to visit and activities to do at a given destination.
Include details such as:
- Top attractions and landmarks
- Cultural experiences
- Natural sites
- Local cuisine and food experiences
- Off-the-beaten-path recommendations
- Seasonal activities or events if relevant
- Approximate time needed for each attraction

Format your response in a clear, easy-to-read manner with sections.
Base your information on general knowledge about the destination.
Focus on providing a diverse range of options for different interests."""
    )

def create_summary_agent() -> Agent:
    """Create and return the Trip Summarizer agent"""
    return Agent(
        name="Trip Summarizer",
        description="Creates a comprehensive trip plan from all gathered information",
        system_prompt="""You are an AI agent specializing in trip planning and summarization.
        
Your task is to create a comprehensive trip plan by combining and synthesizing information about:
1. Flights and transportation
2. Accommodations
3. Attractions and activities

Create a day-by-day itinerary that makes logical sense, considering:
- Travel times between locations
- A reasonable pace of activities
- Balance between scheduled activities and free time
- Practical considerations like check-in/check-out times
- Budget considerations

Format your response as a clear, well-organized travel plan with daily sections.
Be specific where possible but avoid making up exact details that weren't provided.
Add helpful travel tips and packing suggestions relevant to the destination and activities."""
    )

class TravelPlanner:
    """Main class that coordinates all agents for trip planning"""
    def __init__(self, api_key: str, model_type: str):
        self.api_key = api_key
        self.model_type = model_type
        
        # Initialize the appropriate client based on model type
        if model_type == "claude":
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model_name = "claude-3-7-sonnet-20250219"
        elif model_type == "openai":
            self.client = openai.OpenAI(api_key=api_key)
            self.model_name = "gpt-4o"
        elif model_type == "gemini":
            genai.configure(api_key=api_key)
            self.client = genai
            self.model_name = "gemini-1.5-pro"
        
        # Initialize agents
        self.flight_agent = create_flight_agent()
        self.hotel_agent = create_hotel_agent()
        self.attraction_agent = create_attraction_agent()
        self.summary_agent = create_summary_agent()
        
    def create_base_prompt(self, trip_details: Dict[str, Any]) -> str:
        """Create a base prompt with trip details"""
        trip_length = (trip_details['end_date'] - trip_details['start_date']).days
        
        return f"""
        Plan a trip with the following details:
        - Origin: {trip_details['origin']}
        - Destination: {trip_details['destination']}
        - Departure Date: {trip_details['start_date'].strftime('%B %d, %Y')}
        - Return Date: {trip_details['end_date'].strftime('%B %d, %Y')}
        - Trip Duration: {trip_length} days
        - Budget Level: {trip_details['budget']}
        - Number of Travelers: {trip_details['travelers']}
        - Interests: {', '.join(trip_details['interests'])}
        """
    
    def run_flight_agent(self, base_prompt: str) -> str:
        """Run the Flight Finder agent"""
        flight_prompt = base_prompt + "\nFind flight options for this trip between the origin and destination."
        return self.flight_agent.run(self.client, flight_prompt, self.model_type, self.model_name)
    
    def run_hotel_agent(self, base_prompt: str, destination: str, budget: str) -> str:
        """Run the Hotel Explorer agent"""
        hotel_prompt = base_prompt + f"\nFind hotel options in {destination} that fit the budget level of {budget}."
        return self.hotel_agent.run(self.client, hotel_prompt, self.model_type, self.model_name)
    
    def run_attraction_agent(self, base_prompt: str, destination: str, interests: List[str]) -> str:
        """Run the Attraction Scout agent"""
        attraction_prompt = base_prompt + f"\nFind interesting attractions and activities in {destination} that match these interests: {', '.join(interests)}."
        return self.attraction_agent.run(self.client, attraction_prompt, self.model_type, self.model_name)
    
    def run_summary_agent(self, base_prompt: str, flight_result: str, hotel_result: str, attraction_result: str) -> str:
        """Run the Trip Summarizer agent"""
        summary_prompt = f"""
        {base_prompt}
        
        Based on the following information, create a comprehensive day-by-day trip plan:
        
        FLIGHT INFORMATION:
        {flight_result}
        
        HOTEL INFORMATION:
        {hotel_result}
        
        ATTRACTIONS AND ACTIVITIES:
        {attraction_result}
        """
        return self.summary_agent.run(self.client, summary_prompt, self.model_type, self.model_name)
    
    def generate_trip_plan(self, trip_details: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete trip plan using all agents"""
        base_prompt = self.create_base_prompt(trip_details)
        
        # Run all agents
        flight_result = self.run_flight_agent(base_prompt)
        hotel_result = self.run_hotel_agent(base_prompt, trip_details['destination'], trip_details['budget'])
        attraction_result = self.run_attraction_agent(base_prompt, trip_details['destination'], trip_details['interests'])
        summary_result = self.run_summary_agent(base_prompt, flight_result, hotel_result, attraction_result)
        
        # Create trip plan text for download
        trip_length = (trip_details['end_date'] - trip_details['start_date']).days
        trip_plan_text = f"""
        # YOUR TRIP PLAN: {trip_details['origin']} to {trip_details['destination']}
        
        ## Trip Details
        - **Origin**: {trip_details['origin']}
        - **Destination**: {trip_details['destination']}
        - **Dates**: {trip_details['start_date'].strftime('%B %d, %Y')} to {trip_details['end_date'].strftime('%B %d, %Y')}
        - **Duration**: {trip_length} days
        - **Travelers**: {trip_details['travelers']}
        - **Budget**: {trip_details['budget']}
        - **Interests**: {', '.join(trip_details['interests'])}
        
        ## Flight Information
        {flight_result}
        
        ## Accommodation Information
        {hotel_result}
        
        ## Attractions and Activities
        {attraction_result}
        
        ## Complete Day-by-Day Itinerary
        {summary_result}
        """
        
        # Return all results
        return {
            'flight_result': flight_result,
            'hotel_result': hotel_result,
            'attraction_result': attraction_result,
            'summary_result': summary_result,
            'trip_plan_text': trip_plan_text,
            'errors': {
                'flight_error': self.flight_agent.error,
                'hotel_error': self.hotel_agent.error,
                'attraction_error': self.attraction_agent.error,
                'summary_error': self.summary_agent.error
            }
        }
        
if __name__ == "__main__":
    # This allows testing the core logic separately from the UI
    print("TravelPlanner module imported. Use this module with the UI for full functionality.")