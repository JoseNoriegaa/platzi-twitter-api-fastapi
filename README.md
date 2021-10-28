# Platzi - Twitter API
> This project is part of the course "[Clases del Curso de FastAPI: Modularización, Datos Avanzados y Errores
](https://platzi.com/clases/fastapi-modularizacion-datos/)" of "[Platzi](https://platzi.com)"

## Table of Contents:
- [Description](#description)
  - [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#run-it-locally)


## Description
This is project is a simple REST API made with FastAPI for learning purposes.

### Features
Features included:
- Data modeling with pydantic.
- Data validation.
- CRUD of users.
- CRUD of Tweets.
- Data persistance with JSON files (JSON files as database)


## Requirements:
- Python >= 3.6

## Installation
1. Clone or download de repository:
    ```
    $ git clone https://github.com/JoseNoriegaa/plazi-twitter-api-fastapi
    ```

2. Open the console inside the project directory and create a virtual environment.
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```

3. Install the app
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

## Run it locally
```
(venv) $ uvicorn main:app --reload
```

## Basic Usage
Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.
