import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def format(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formated = []
    for question in questions:
        formated.append({
            'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'category': question.category,
            'difficulty': question.difficulty
        })
    return formated[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
          "Access-Control-Allow_Headers", "Content-Type,Authorization,true")
        response.headers.add(
          "Access-Control-Allow-Methods", "GET,POST,DELETE")
        return response

    @app.route('/categories')
    def all_quiz_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
          category.id: category.type for category in categories}
        return jsonify({
          "categories": formatted_categories
        })

    @app.route('/questions')
    def all_quiz_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formated_cat = {category.id: category.type for category in categories}
        listed_questions = format(request, questions)
        if len(listed_questions) == 0:
            abort(404)
        return jsonify({
          "questions": listed_questions,
          "total_questions": len(questions),
          "categories": formated_cat
        })

    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
              Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.id).all()
            formated_cat = {
              category.id: category.type for category in categories}

            listed_questions = format(request, questions)

            if len(listed_questions) == 0:
                abort(404)

            return jsonify({
              "questions": listed_questions,
              "total_questions": len(questions),
              "categories": formated_cat
            })

        except Exception as e:
            print("error " + str(e))
            abort(422)

    @app.route('/questions', methods=["POST"])
    def create_or_search_question():

        # getting information
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_question_category = body.get("category", None)
        new_question_difficulty = body.get("difficulty", None)
        search_term = body.get("searchTerm", None)

        # query and formatting
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formated_cat = {category.id: category.type for category in categories}

        try:
            if search_term is not None:
                # if the search was empty return all questions
                if search_term == "":
                    listed_questions = format(request, questions)

                    if len(listed_questions) == 0:
                        abort(404)

                    return jsonify({
                      "questions": listed_questions,
                      "total_questions": len(questions),
                      "categories": formated_cat
                      })

                # searching the questions and returning the list
                selections = Question.query.order_by(
                  Question.id).filter(
                    Question.question.ilike(f"% {search_term} %"))
                current_questions = format(request, selections)
                if len(current_questions) == 0:
                    abort(404)

                return jsonify({
                  "questions": current_questions,
                  "total_questions": len(questions),
                  "categories": formated_cat
                  })

            # this is for checking
            # if he was submitting new question or searching
            elif (new_question is not None) & (new_question_category is not None):
                if new_answer == "":
                    abort(422)
                question = Question(
                  question=new_question,
                  answer=new_answer,
                  category=new_question_category,
                  difficulty=new_question_difficulty
                  )
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                categories = Category.query.order_by(Category.id).all()
                formated_cat = {
                  category.id:
                  category.type for category in categories
                  }

                listed_questions = format(request, questions)

                if len(listed_questions) == 0:
                    abort(404)

                return jsonify({
                  "questions": listed_questions,
                  "total_questions": len(questions),
                  "categories": formated_cat
                  })

        except Exception as e:
            print("error info: " + str(e))
            abort(422)

    @app.route('/categories/<category_id>/questions')
    def selected_category(category_id):
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        formated_cat = {category.id: category.type for category in categories}
        selections = Question.query.order_by(
          Question.id).filter(
            Question.category == category_id).all()
        listed_questions = format(request, selections)
        if len(listed_questions) == 0:
            abort(404)

        return jsonify({
              "questions": listed_questions,
              "total_questions": len(questions),
              "categories": formated_cat
              })

    @app.route('/quizzes', methods=["POST"])
    def quiz():
        body = request.get_json()
        category_id = body.get("quiz_category", None).get("id", None)
        previous_questions = body.get("previous_questions", None)
        if category_id == 0:
            questions = Question.query.order_by(Question.id).all()
        elif category_id is not None:
            questions = Question.query.order_by(
              Question.id).filter(
                Question.category == category_id).all()
        if len(questions) == 0:
                    abort(404)
        if previous_questions is None:
            next_question = format(request, questions)
            return jsonify({
              "question": random.choice(next_question),
              "forceEnd": True
            })
        else:
            next_question = questions
            for previous_question in previous_questions:
                for remove_question in next_question:
                    test = previous_question == remove_question.id
                    if test:
                        next_question.remove(remove_question)
            next_question = format(request, questions)
            return jsonify({
              "question": random.choice(next_question)
            })

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"error": 422, "message": "unprocessable"}),
            422,
        )

    return app
