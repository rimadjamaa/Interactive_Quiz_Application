import requests
from models.models import Category, db, Quiz, Question

def fetch_questions(api_url, quiz_title):
    response = requests.get(api_url)
    data = response.json()
    

    if data['response_code'] == 0:  # Successful response
        for item in data['results']:
            # Check if the category exists
            category_name = item['category']
            category = Category.query.filter_by(name=category_name).first()
        
            # If not, create and add it
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()


            quiz = Quiz(title=quiz_title, description="Generated from Trivia API", category_id=category.id)
            db.session.add(quiz)
            db.session.commit()  # Save the quiz to get its ID

            
             # Ensure we have enough incorrect answers
            choice1 = item['incorrect_answers'][0] if len(item['incorrect_answers']) > 0 else None
            choice2 = item['incorrect_answers'][1] if len(item['incorrect_answers']) > 1 else None
            choice3 = item['incorrect_answers'][2] if len(item['incorrect_answers']) > 2 else None
            
            question = Question(
                quiz_id=quiz.id,
                question_text=item['question'],
                choice1=choice1,
                choice2=choice2,
                choice3=choice3,
                choice4=item['correct_answer'],
                answer=item['correct_answer']
            )
            db.session.add(question)
        db.session.commit()
        print(f"Quiz '{quiz_title}' and its questions have been added.")
    else:
        print("Failed to fetch questions from the API.")


