from flask import Flask, request, jsonify
from flask_cors import CORS 



app = Flask(__name__)
CORS(app) 

# Sample data for courses, vacations, diet plans, and automobiles
courses = [
    {"name": "Python Programming", "subject": "Programming", "level": "Beginner"},
    {"name": "Data Science Bootcamp", "subject": "Data Science", "level": "Intermediate"},
    {"name": "Web Development", "subject": "Programming", "level": "Beginner"},
]

vacations = [
    {"name": "Beach Getaway", "destination": "Hawaii", "price": "$$$"},
    {"name": "Mountain Adventure", "destination": "Swiss Alps", "price": "$$$"},
    {"name": "City Exploration", "destination": "New York", "price": "$$"},
]

diet_plans = [
    {"name": "Keto Diet", "type": "Keto", "description": "Low carb diet focused on high-fat intake."},
    {"name": "Vegan Diet", "type": "Vegan", "description": "Plant-based diet avoiding all animal products."},
    {"name": "Paleo Diet", "type": "Paleo", "description": "Diet based on foods similar to those eaten during the Paleolithic era."},
]

automobiles = [
    {"name": "Toyota Camry", "type": "Sedan", "price": 24000},
    {"name": "Ford F-150", "type": "Truck", "price": 30000},
    {"name": "Tesla Model 3", "type": "Electric", "price": 40000},
]

@app.route('/recommend', methods=['POST'])
def recommend():
    user_pref = request.json
    recommendation_type = user_pref.get('type')

    if recommendation_type == 'course':
        subject = user_pref.get('subject')
        # Filter courses based on subject
        matching_courses = [course for course in courses if course['subject'].lower() == subject.lower()]
        if not matching_courses:
            return jsonify({'message': "No matching courses found."}), 404
        top_course = matching_courses[0]  # Simple selection
        message = f"Recommended Course: {top_course['name']} - Level: {top_course['level']}"

    elif recommendation_type == 'vacation':
        destination = user_pref.get('destination')
        # Filter vacations based on destination
        matching_vacations = [vacation for vacation in vacations if vacation['destination'].lower() == destination.lower()]
        if not matching_vacations:
            return jsonify({'message': "No matching vacations found."}), 404
        top_vacation = matching_vacations[0]  # Simple selection
        message = f"Recommended Vacation: {top_vacation['name']} - Destination: {top_vacation['destination']}"

    elif recommendation_type == 'diet_plan':
        diet_type = user_pref.get('diet_type')
        # Filter diet plans based on type
        matching_diets = [diet for diet in diet_plans if diet['type'].lower() == diet_type.lower()]
        if not matching_diets:
            return jsonify({'message': "No matching diet plans found."}), 404
        top_diet = matching_diets[0]  # Simple selection
        message = f"Recommended Diet Plan: {top_diet['name']} - Description: {top_diet['description']}"

    elif recommendation_type == 'automobile':
        budget = user_pref.get('budget')
        # Filter automobiles based on budget
        matching_cars = [car for car in automobiles if car['price'] <= budget]
        if not matching_cars:
            return jsonify({'message': "No matching automobiles found."}), 404
        top_car = matching_cars[0]  # Simple selection
        message = f"Recommended Automobile: {top_car['name']} - Price: ${top_car['price']}"

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
