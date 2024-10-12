import requests
from models import UserPreference

def test_send_preference(assistant_address, user_id, preference):
    """Test sending user preference."""
    response = requests.post(f"{assistant_address}/preferences", json={
        "user_id": user_id,
        "preference": preference
    })
    print("Send Preference Response:", response.json())

def test_send_request(assistant_address, user_id, domain, context_data):
    """Test sending context request."""
    response = requests.post(f"{assistant_address}/request", json={
        "user_id": user_id,
        "domain": domain,
        "context_data": context_data
    })
    print("Send Request Response:", response.json())

if __name__ == "__main__":
    # Example usage
    assistant_address = "http://0.0.0.0:8000/submit"  # Replace with your actual address
    user_id = "user1"
    preference = "I prefer vegan food options"
    domain = "food"
    context_data = "Looking for dinner suggestions."

    # Test sending preference
    test_send_preference(assistant_address, user_id, preference)

    # Test sending request
    test_send_request(assistant_address, user_id, domain, context_data)
