from pydantic import BaseModel
from uagents import Agent, Protocol, Context
from models import UserPreference, ContextRequest, ContextResponse

# Define your message models using pydantic for schema generation

class UserPreference(BaseModel):
    user_id: str
    preference: str

class ContextRequest(BaseModel):
    user_id: str
    domain: str
    context_data: str

class ContextResponse(BaseModel):
    recommendation: str

# Define the assistant agent
def main():
    assistant_agent = Agent(
        name="assistant_agent",
        port=8000,  # Agent will be hosted on port 8000
        endpoint=["http://0.0.0.0:8000"]  # Accessible from any IP address
    )
    
    # Define the protocol
    protocol = Protocol("AssistantProtocol", "1.0.0")

    # Handler for UserPreference messages
    @protocol.on_message(model=UserPreference)
    async def handle_user_preference(ctx: Context, sender: str, msg: UserPreference):
        # Process user preference and store it if needed
        print(f"Received preference from {sender}: {msg.preference}")
        # Respond or perform actions accordingly

    # Handler for ContextRequest messages
    @protocol.on_message(model=ContextRequest)
    async def handle_context_request(ctx: Context, sender: str, msg: ContextRequest):
        # Process context request and generate a recommendation
        print(f"Received request from {sender}: {msg.context_data}")
        recommendation = generate_recommendation(msg.domain, msg.context_data)
        
        # Send back a ContextResponse
        response = ContextResponse(recommendation=recommendation)
        await ctx.send(sender, response)

    # Include the protocol in the agent
    assistant_agent.include(protocol)
    
    # Start the agent
    print(f"Assistant agent running at http://0.0.0.0:8000")
    assistant_agent.run()

# Function to generate recommendations (you can modify this logic as needed)
def generate_recommendation(domain, context_data):
    if domain == "food":
        return "Try a healthy salad or a smoothie!"
    elif domain == "entertainment":
        return "How about watching a new movie on Netflix?"
    else:
        return f"No specific recommendation for the domain: {domain}"

if __name__ == "__main__":
    main()
