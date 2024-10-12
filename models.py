import streamlit as st
import asyncio
import nest_asyncio
from uagents import Agent, Protocol, Context
# from models import ContextRequest, ContextResponse
import time

# Apply nest_asyncio to handle async operations in Streamlit
nest_asyncio.apply()

class StreamlitAgent:
    def __init__(self):
        self.agent = None
        self.protocol = None
        self.response_received = None

    def initialize_agent(self):
        """Initializes the agent and sets up the communication protocol."""
        if self.agent is None:
            self.agent = Agent(
                name="streamlit_client",
                port=8001,
                endpoint=["http://0.0.0.0:8000/submit"],  # Corrected the address here
            )

            self.protocol = Protocol("StreamlitProtocol", "1.0.0")

            @self.protocol.on_message(model=ContextResponse)
            async def handle_response(ctx: Context, sender: str, msg: ContextResponse):
                self.response_received = msg.recommendation

            self.agent.include(self.protocol)

    def send_preference(self, assistant_address, user_id, preference):
        """Sends user preference to the assistant."""
        from models import UserPreference  # Avoid circular imports
        self.initialize_agent()
        if not self.agent.is_running:
            asyncio.run(self.agent.start())  # Start the agent synchronously

        message = UserPreference(user_id=user_id, preference=preference)
        asyncio.run(self.agent.send(assistant_address, message))  # Send message synchronously
        time.sleep(2)  # Add some wait time to simulate async

    def send_request(self, assistant_address, user_id, domain, context_data):
        """Sends context request to the assistant."""
        from models import ContextRequest  # Move the import here to avoid circular imports
        self.initialize_agent()
        if not self.agent.is_running:
            asyncio.run(self.agent.start())

        self.response_received = None
        message = ContextRequest(
            user_id=user_id,
            domain=domain,
            context_data=context_data
        )

        asyncio.run(self.agent.send(assistant_address, message))  # Send request synchronously

        # Wait for response with timeout
        timeout = 10
        start_time = time.time()
        while self.response_received is None:
            time.sleep(0.1)
            if time.time() - start_time > timeout:
                return "Timeout waiting for response"

        return self.response_received

def main():
    st.title("Context-Aware Assistant Interface")

    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = StreamlitAgent()

    # Input fields
    with st.form("assistant_config"):
        st.subheader("Configuration")
        assistant_address = st.text_input(
            "Assistant Address",
            help="Enter the address shown when running main1.py"
        )
        user_id = st.text_input("User ID", value="user1")
        st.form_submit_button("Save Configuration")

    # Preference setting
    with st.form("preference_form"):
        st.subheader("Set User Preferences")
        preference = st.text_input(
            "Enter Preference",
            placeholder="e.g., I prefer healthy food options"
        )
        submit_preference = st.form_submit_button("Set Preference")

        if submit_preference and assistant_address and preference:
            with st.spinner("Setting preference..."):
                try:
                    st.session_state.agent.send_preference(
                        assistant_address, user_id, preference
                    )
                    st.success("Preference set successfully!")
                except Exception as e:
                    st.error(f"Error setting preference: {str(e)}")

    # Context request
    with st.form("request_form"):
        st.subheader("Make a Request")
        domain = st.text_input(
            "Domain",
            placeholder="e.g., food, entertainment, work"
        )
        context_data = st.text_area(
            "Context",
            placeholder="e.g., Looking for dinner suggestions, currently at home"
        )
        submit_request = st.form_submit_button("Get Recommendations")

        if submit_request and assistant_address and domain and context_data:
            with st.spinner("Getting recommendations..."):
                try:
                    response = st.session_state.agent.send_request(
                        assistant_address, user_id, domain, context_data
                    )
                    st.markdown("### Recommendation:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error getting recommendations: {str(e)}")

if __name__ == "__main__":
    main()

from pydantic import BaseModel

class UserPreference(BaseModel):
    user_id: str
    preference: str

class ContextRequest(BaseModel):
    user_id: str
    domain: str
    context_data: str

class ContextResponse(BaseModel):
    recommendation: str

