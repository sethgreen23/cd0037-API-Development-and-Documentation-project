# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

### Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET '/questions'`

- Fetch a dictionary of all available questions of all categories paginated (10 questions per page)
- Request Arguments which is optional indicates the number of current page: page
- Return: An object with respective keys "categories", "current_category", "questions", "total_questions" and "success"

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "current_category": null,
  "total_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "How long does it take to hard boil an egg?",
      "answer": "Seven minutes",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 1,
      "question": "How many rides are at Disney World?",
      "answer": "46",
      "category": 5,
      "difficulty": 3
    }
  ]
}
```

`DELETE '/questions/<question_id>'`

- DELETE an existing question from the available questions in the database
- Request Arguments : question_id
- Return: An object with unique key "success"

```json
{
  "success": true
}
```

`POST '/questions'`

- Fetches a dictionary of all availlable question related to a spacific string pattern
- Request Arguments :{'searchTerm':string}
- Return: An object with respective keys "success", "current_category", "total_questions" and "questions"

```json
{
  "success": true,
  "current_category": null,
  "total_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "How long does it take to hard boil an egg?",
      "answer": "Seven minutes",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 1,
      "question": "How many rides are at Disney World?",
      "answer": "46",
      "category": 5,
      "difficulty": 3
    }
  ]
}
```

`POST '/questions'`

- Add a new question to the database
- Request Arguments :{'question':string, 'answer':string, 'difficulty':int, 'category':int}
- Return: An object with unique key "success"

```json
{
  "success": true
}
```

`GET '/categories/<category_id>/questions'`

- Fetch a dictionary of all available questions for a specifc category
- Request Arguments :category_id
- Return: An object with respective keys "success", "questions", "total_questions" and "current_category"

```json
{
  "success": true,
  "current_category": 1,
  "total_questions": 2,
  "questions": [
    {
      "id": 1,
      "question": "How long does it take to hard boil an egg?",
      "answer": "Seven minutes",
      "category": 1,
      "difficulty": 1
    },
    {
      "id": 1,
      "question": "What’s the hardest rock?",
      "answer": "A diamond",
      "category": 5,
      "difficulty": 3
    }
  ]
}
```

`POST '/quizzes'`

- Fetch one random question from a specific category.We dont pick up an already asked question.When we go throw all the question a None question is returned that ends the game and show the final score.
- Request Arguments :{'previous_questions':string, 'quiz_category': {id:int, type:string}}
- Return: An object with respective keys "success" and "question"

```json
{
  "success": true,
  "question": {
    "id": 1,
    "question": "What’s the hardest rock?",
    "answer": "A diamond",
    "category": 5,
    "difficulty": 3
  }
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
