import streamlit as st
import asyncio
import nest_asyncio
from uagents import Agent, Protocol, Context
# from models import UserPreference, ContextRequest, ContextResponse
import time
from main1 import ContextRequest, ContextResponse, UserPreference

# Apply nest_asyncio to handle async operations in Streamlit
nest_asyncio.apply()

class StreamlitAgent:
    def __init__(self):
        self.agent = None
        self.protocol = None
        self.response_received = None
        
    def initialize_agent(self):
        if self.agent is None:
            self.agent = Agent(
                name="streamlit_client",
                port=8001,
                endpoint=["http://0.0.0.0:8000/submit"],
            )
            
            self.protocol = Protocol("StreamlitProtocol", "1.0.0")
            
            @self.protocol.on_message(model=ContextResponse)
            async def handle_response(ctx: Context, sender: str, msg: ContextResponse):
                self.response_received = msg.recommendation
                
            self.agent.include(self.protocol)

    async def start_agent(self):
        if self.agent is not None and not self.agent._running:
            await self.agent.start()  # Start the agent asynchronously

    

    def send_request(self, assistant_address, user_id, domain, context_data):
        from models import ContextRequest  # Move the import here to avoid circular imports
        self.initialize_agent()
        asyncio.run(self.start_agent())  # Start the agent

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
