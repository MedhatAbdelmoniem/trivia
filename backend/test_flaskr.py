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
        self.database_name = "trivia"
        self.database_path = 'postgresql://localhost:5000/trivia'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    

    def test_getting_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["categories"])


    def test_getting_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])


    def test_post_category_error(self):
        res = self.client().post("/categories")

        self.assertEqual(res.status_code,405)


    def test_delete_unexisted_question(self):
        res = self.client().delete("/questions/1000")

        self.assertEqual(res.status_code,422)


    def test_search_question(self):
         res = self.client().post("/questions", json={"searchTerm": "title"})
         data = json.loads(res.data)

         self.assertEqual(res.status_code,200)
         self.assertEqual(len(data["questions"]),1)


    def test_create_question(self):
        res = self.client().post("/questions", json={"question": "what does water boil at","answer":"100","category":"1","difficulty":"1"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])


    def test_create_false_question_answer(self):
        res = self.client().post("/questions", json={"question": "what does water boil at","answer":"","category": "1","difficulty":"1"})

        self.assertEqual(res.status_code,422)

    def test_select_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["questions"])


    def select_unexisted_category(self):
     res = self.client().get("/categories/1000/questions")
    
     self.assertEqual(res.status_code,404)

    def test_quiz(self):
        res = self.client().post("/quizzes", json={"quiz_category": {'type': 'Science','id': 1},"previous_questions":None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["question"])


    def test_quiz_with_false_category(self):
        res = self.client().post("/quizzes", json={"quiz_category": {'type': 'NotFound','id': 1000},"previous_questions":None})

        self.assertEqual(res.status_code,404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()