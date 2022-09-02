import os
import json
from tracemalloc import start
from winreg import QueryInfoKey
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#create pagination function to take care of the pagination process
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

#format the selection of categories
def format_categories(selection):
    categories = {category.id:category.type for category in selection}
    return categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins":"*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,PUT,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    #get all the categorie 
    @app.route("/categories", methods=["GET"])
    def retrieve_all_categories():
        categories = Category.query.order_by(Category.type).all()
        if len(categories) == 0:
            abort(404)
        
        return jsonify({
            'success':True,
            'categories' : format_categories(categories)
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    #get all questions ordered by id and paginated
    #the categorie are ordered by type for the alphabetic order
    @app.route("/questions", methods=['GET'])
    def retrieve_paginated_questions():
        questions = Question.query.order_by(Question.id).all()
        
        categories = Category.query.order_by(Category.type).all()

        questions_format = paginate_questions(request, questions)
        
        if len(questions_format) == 0:
            abort(404)

        return jsonify({
            'success':True,
            'questions': questions_format,
            'total_questions':len(questions),
            'categories': format_categories(categories),
            'current_category':None
        })
        

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    #delete a question
    @app.route('/questions/<question_id>',methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id==question_id).one_or_none()
            # print(question)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success':True
            })
        except:
            abort(422)
        
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    #it treats the post method of searching question with specific patern and the creation of question
    @app.route('/questions', methods=['POST'])
    def add_search_question():
        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        category = body.get('category',None)
        difficulty = body.get('difficulty',None)
        searchTerm = body.get('searchTerm',None)
        
        try:
            #if the serach term exists then it is a search
            if searchTerm:
                
                questions_selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(searchTerm))).all()
                
                totalQuestion = len(questions_selection)
                currentCategory = None
                current_questions_list = paginate_questions(request, questions_selection)
                return jsonify({
                    'success':True,
                    'questions':current_questions_list,
                    'total_questions':totalQuestion,
                    'current_category':currentCategory
                })
                #if not it is a creation
            else:
                                        
                    question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                    question.insert()

                    return jsonify({
                        'success':True
                    })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    #Done in the previous function
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    #get all questions by specific category
    @app.route('/categories/<categorie_id>/questions', methods=['GET'])
    def retrieve_questions_by_categories(categorie_id):
        questions_by_category = Question.query.order_by(Question.id).filter(Question.category==categorie_id).all()
        
        if len(questions_by_category)==0:
            abort(404)

        totalQuestions = len(questions_by_category)
        currentCategory = Category.query.filter_by(id=categorie_id).one_or_none()
        if currentCategory:
            currentCategory = currentCategory.type
        questions_by_category_format = paginate_questions(request,questions_by_category)

        return jsonify({
            'success':True,
            'questions':questions_by_category_format,
            'total_questions':totalQuestions,
            'current_category': currentCategory
        }) 

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    #play quiz function
    @app.route('/quizzes', methods=['POST'])
    def questions_to_play_quiz():
        body = request.get_json()
        if not('previous_questions' in body and 'quiz_category' in body):
            abort(422)

        questions_previous_id_list = body.get('previous_questions')
        quiz_category = body.get('quiz_category')
        
        next_question = None
        question_list = []
        
        # here we treat the cases if chosing a specific category or to chose all question
        #here we chose all question where the reponse is {'type':'click' , 'id':0}
        if quiz_category['id'] == 0:
            question_list = Question.query.filter(Question.id.not_in(questions_previous_id_list)).all()
        #here the chose a specific category like {'type': 'Science', 'id':1}
        else:
            question_list = Question.query.filter(Question.category==quiz_category['id']).filter(Question.id.not_in(questions_previous_id_list)).all()
        
        #till we have a list of unselected of question we  chose from it
        #once we went throw all the question we return a None question to exit the quiz and to get the score
        if len(question_list) > 0:
            next_question = question_list[random.randint(0, len(question_list)-1)].format()

        return jsonify({
            'success':True,
            'question':next_question

        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    
    return app

