import asyncio
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from datetime import datetime

# Define UserPreference model
class UserPreference(Model):
    cuisine: str
    price_range: str
    dietary_restrictions: list[str]

# Define Restaurant model
class Restaurant(Model):
    name: str
    cuisine: str
    price_range: str
    rating: float
    address: str

# Simulated restaurant database
restaurants = [
    Restaurant(name="Pasta Paradise", cuisine="Italian", price_range="100-500", rating=4.5, address="123 Main St"),
    Restaurant(name="Sushi Sensation", cuisine="Japanese", price_range="500-800", rating=4.7, address="456 Oak Ave"),
    Restaurant(name="Burger Bliss", cuisine="American", price_range="800-1000", rating=4.2, address="789 Elm St"),
    Restaurant(name="Veggie Delight", cuisine="Vegetarian", price_range="123-999", rating=4.4, address="101 Pine Rd"),
    Restaurant(name="Spice Avenue", cuisine="Indian", price_range="123-567", rating=4.6, address="202 Maple Ln")
]

# Create an agent
recommendation_agent = Agent(
    name="restaurant_recommender",
    seed="restaurant_recommendation_seed"
)

# Fund the agent if needed
fund_agent_if_low(recommendation_agent.wallet.address())

@recommendation_agent.on_message(model=UserPreference)
async def handle_user_preference(ctx: Context, sender: str, msg: UserPreference):
    ctx.logger.info(f"Received user preference: {msg}")
    
    # Filter restaurants based on user preferences
    matching_restaurants = [
        r for r in restaurants
        if r.cuisine.lower() == msg.cuisine.lower() and r.price_range == msg.price_range
    ]
    
    if not matching_restaurants:
        await ctx.send(sender, "Sorry, no matching restaurants found.")
        return
    
    # Sort by rating and select the top restaurant
    top_restaurant = max(matching_restaurants, key=lambda r: r.rating)
    
    # Get current time for context
    current_time = datetime.now().strftime("%H:%M")
    
    # Prepare recommendation message
    recommendation = (
        f"Based on your preferences, I recommend {top_restaurant.name}!\n"
        f"Cuisine: {top_restaurant.cuisine}\n"
        f"Price Range: {top_restaurant.price_range}\n"
        f"Rating: {top_restaurant.rating}\n"
        f"Address: {top_restaurant.address}\n"
        f"Current Time: {current_time}"
    )
    
    await ctx.send(sender, recommendation)

# print("Restaurant recommendation agent created and ready to receive messages.")

# Mock logger class
class MockLogger:
    def info(self, message):
        print(f"INFO: {message}")

# Mock context class for testing
class MockContext(Context):
    def __init__(self):
        # Provide dummy values for the required arguments
        super().__init__(address='mock_address', identifier='mock_identifier', name='mock_name',
                         storage=None, resolve=None, identity=None, wallet=None, ledger=None, queries=None)
        self._mock_logger = MockLogger()  # Assign the mock logger to a different name

    @property
    def logger(self):
        return self._mock_logger  # Return the mock logger when accessed

    async def send(self, sender, message):
        print(f"Sender: {sender}, Message: {message}")

# Test function to simulate sending a user preference

cuisine = input("what type of cuisine would you like to have?")
price_range = input("what price range would you like to have?")
async def test_agent():
    user_preference = UserPreference(
        cuisine=cuisine,
        price_range=price_range,
        dietary_restrictions=[]
    )
    
    # Create a mock context
    mock_context = MockContext()
    
    # Call the handler function directly
    await handle_user_preference(mock_context, "test_user", user_preference)

# Run the test
if __name__ == "__main__":
    asyncio.run(test_agent())
