import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format('postgres','123','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #create a question to use it in testing the creation
        self.new_question = {'question':'How long does it take to hard boil an egg?', 'answer':'Seven minutes', 'difficulty':1, 'category':1}


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #test the get paginated questions for 1 page
    def test_get_paginated_question(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
    
    #test the get paginated questions for number of page beyound the existing number of pages
    def test_404_sent_requesting_beyound_valid_page(self):
        res = self.client().get("/quesions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    #test get categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    #create a question and delete it 
    def test_delete_question(self):
        #prepare the argument of the question
        question = 'What is Ariana Grande’s brother’s name?'
        answer = 'Frankie'

        #create the question object 
        question_to_delete = Question(question=question, answer=answer, difficulty=3, category=5)
        #insert th question
        question_to_delete.insert()
        #use the inserted question on the deletion to preserve the integrity of the test database
        res = self.client().delete('/questions/{}'.format(question_to_delete.id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #test the deletion for a quesion id beyoud the existing ids
    def test_422_sent_requesting_beyound_existing_question(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    #test the creation of new question
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #test if the creation fails even though we wont get 
    def test_422_if_question_creations_fails(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        pass
    
    #test the question search with results
    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={'searchTerm':'?'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    
    #test the question search without results
    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={'searchTerm':'azerty'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)

    #test get questions per category for this i used the category with id=1
    def test_get_questions_per_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    #test get question per category with a category id beyoud the existing id
    def test_404_sent_requesting_beyound_existing_categories(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Resource not found')

    #testing the quiz playing using all question choice
    def test_questions_to_play_quiz_using_all_questions(self):
        new_quiz_with_all_questions = {'previous_questions':[], 'quiz_category': {'type':'click', 'id':0}}
        res = self.client().post('/quizzes', json=new_quiz_with_all_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #testing the quiz playing using a specic category from the existing one her i chosed the first one
    def test_questions_to_play_quiz_using_a_category(self):
        new_quiz_with_specific_category = {'previous_questions':[], 'quiz_category':{'type':'Science','id':1}}
        res = self.client().post('/quizzes',json=new_quiz_with_specific_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #testing th quiz playing without sending the category all or specific category
    def test_404_questions_to_play_quiz(self):
        new_quiz = {'previous_questions':[]}
        res = self.client().post('/quizzes', json=new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()