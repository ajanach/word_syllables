# German word syllables

This project explains and demonstrates the process of creating an algorithm that allows for the decomposition of words into syllables in the German language. Specifically, it documents specific implicit and explicit linguistic knowledge and its conversion and formalization for the purpose of creating a syllabification algorithm. The final goal of the project is to create an algorithm and application that can decompose any German word into syllables by adding a space between adjacent syllables for any input text. The project will use Python programming language to formally write the rules based on the explicit and implicit knowledge collected by linguists for the German language and use it to create an algorithm for syllable decomposition that adheres to the rules of the German language and takes into account that the process is not always straightforward.

## Installation
To run the app word_syllables, satisfy the requirements:
```shell
pip install -r requirements.txt
```

## Set Environment Variables
```shell
export FLASK_APP=app.py
export FLASK_ENV=development
```

## Start Server
```shell
flask run
```
or run this command:
```shell
python -m flask run
```
