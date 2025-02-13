import os
import streamlit as st
from crewai import Crew
from textwrap import dedent
from project1.agents import TravelAgents  # Updated import statement
from project1.tasks import TravelTasks  # Updated import statement
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service.json"

# Page Configuration
st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="centered")

# Custom Styling
st.markdown(
    """
    <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
        }
        .stTextInput input {
            font-size: 16px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Title
st.title("🌍 AI-Powered Trip Planner")
st.subheader("Plan your Dream trip Effortlessly with AI!")

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TravelAgents()
        tasks = TravelTasks()

        expert_travel_agent = agents.expert_travel_agent()
        city_selection_expert = agents.city_selection_expert()
        local_tour_guide = agents.Local_tour_guide()

        plan_trip = tasks.plan_trip(expert_travel_agent, self.cities, self.date_range, self.interests)
        identify_city = tasks.identify_city(city_selection_expert, self.origin, self.cities, self.date_range, self.interests)
        gather_city_info = tasks.gather_city_info(local_tour_guide, self.cities, self.date_range, self.interests)

        crew = Crew(
            agents=[expert_travel_agent, city_selection_expert, local_tour_guide],
            tasks=[plan_trip, identify_city, gather_city_info],
            verbose=True,
        )

        result = crew.kickoff()
        return result

# User Inputs
with st.form("trip_form"):
    origin = st.text_input("✈️ Where are you traveling from?")
    cities = st.text_area("🏙️ Which cities are you interested in visiting?")
    start_date = st.date_input("📅 Start Date")
    end_date = st.date_input("📅 End Date")
    interests = st.text_area("🎯 Your Interests & Hobbies?")
    submit_button = st.form_submit_button("🚀 Plan My Trip")

# Combine start and end dates into a single range string
date_range = f"{start_date} to {end_date}"

# Trigger the AI trip planner
if submit_button:
    if origin and cities and start_date and end_date and interests:
        with st.spinner("🧳 Planning your trip... Please wait..."):
            trip_crew = TripCrew(origin, cities, date_range, interests)
            result = trip_crew.run()

        st.success("✅ Your AI-generated trip plan is ready!")
        st.markdown("## 📌 Your Trip Plan:")
        st.write(result)
    else:
        st.warning("⚠️ Please fill in all the required fields!")
