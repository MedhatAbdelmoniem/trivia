how to start the project:

-First run the server by setting the FLASK_APP=flaskr and run it by flask run
-second run python text_flaskr to test for errors
-third run npm start in the front end folder to start the site

api documentation :
This api is to provide the questions and its info for the site

when the page loads it should call two route /categories and /questions:


the /categories route takes nothing
but it returns all the categories: 

    {
      "categories": []
    }

----------------------------------------------------------------------------------------------

the /questions route takes nothing
but it returns all the questions 




    {
      "questions": [],
      "total_questions":len([]),
      "categories": []
    }



----------------------------------------------------------------------------------------------
when /questions/<question_id> is called when deleting it should remove the question with that id

the question_id is the id of the wished question to be deleted.


----------------------------------------------------------------------------------------------
when /categories/<category_id>/questions is called it should return all questions with this category id

        {
          "questions": [],
          "total_questions":len([]),
          "categories": []
        }


----------------------------------------------------------------------------------------------

when /questions is called with POST method to create a new question it should add this question to the database

it takes the question, its answer , the category the question belong to and its difficulty.
the id of the question is created automatically

----------------------------------------------------------------------------------------------


when /questions is called with POST method to search it should return all questions if it include the search word and if it was 
empty it returns all questions

          {
          "questions": [],
          "total_questions":len([]),
          "categories": []
          } 

it takes the search word

----------------------------------------------------------------------------------------------

if there was no questions in all cases it should return 404 error with:

{"error": 404, "message": "resource not found"}

----------------------------------------------------------------------------------------------

if the request is unprocessable it should return 422 error with:


{"error": 422, "message": "unprocessable"}