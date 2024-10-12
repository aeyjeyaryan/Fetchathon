import streamlit as st
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from datetime import datetime
import asyncio

class UserPreference(Model):
    cuisine: str
    price_range: str
    dietary_restrictions: list[str]

class Restaurant(Model):
    name: str
    cuisine: str
    price_range: str
    rating: float
    address: str

# Simulated restaurant database
restaurants = [
    Restaurant(name="Pasta Paradise", cuisine="Italian", price_range="$$", rating=4.5, address="123 Main St"),
    Restaurant(name="Sushi Sensation", cuisine="Japanese", price_range="$$$", rating=4.7, address="456 Oak Ave"),
    Restaurant(name="Burger Bliss", cuisine="American", price_range="$", rating=4.2, address="789 Elm St"),
    Restaurant(name="Veggie Delight", cuisine="Vegetarian", price_range="$$", rating=4.4, address="101 Pine Rd"),
    Restaurant(name="Spice Avenue", cuisine="Indian", price_range="$$", rating=4.6, address="202 Maple Ln")
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
        if r.cuisine.lower() == msg.cuisine.lower()
        and r.price_range == msg.price_range
    ]
    
    if not matching_restaurants:
        return "Sorry, no matching restaurants found."
    
    # Sort by rating and select the top restaurant
    top_restaurant = max(matching_restaurants, key=lambda r: r.rating)
    
    # Get current time for context
    current_time = datetime.now().strftime("%H:%M")
    
    # Prepare recommendation message
    recommendation = (
        f"Based on your preferences, I recommend {top_restaurant.name}!\
"
        f"Cuisine: {top_restaurant.cuisine}\
"
        f"Price Range: {top_restaurant.price_range}\
"
        f"Rating: {top_restaurant.rating}\
"
        f"Address: {top_restaurant.address}\
"
        f"Current Time: {current_time}"
    )
    
    return recommendation

# Streamlit app
st.title("Restaurant Recommender")

cuisine = st.selectbox("Select cuisine:", ["Italian", "Japanese", "American", "Vegetarian", "Indian"])
price_range = st.select_slider("Select price range:", options=["$", "$$", "$$$"])
dietary_restrictions = st.multiselect("Select dietary restrictions:", ["Vegetarian", "Vegan", "Gluten-free", "None"])

if st.button("Get Recommendation"):
    user_pref = UserPreference(cuisine=cuisine, price_range=price_range, dietary_restrictions=dietary_restrictions)
    
    # Create a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Run the agent's message handler
    recommendation = loop.run_until_complete(handle_user_preference(recommendation_agent.context, "user", user_pref))
    
    st.write(recommendation)

# Run the Streamlit app
if __name__ == "__main__":
    print("Streamlit app is ready. Run it with: streamlit run <filename>.py")

# Save the code to a file
with open("restaurant_recommender_app.py", "w") as f:
    f.write(open(__file__).read())

print("Streamlit app code has been saved to 'restaurant_recommender_app.py'")