# German word syllables

The final goal of the project is to create an algorithm and application that can split any German word into syllables by adding a space between adjacent syllables for any input text. The project uses the Python programming language to formally write the rules based on the explicit and implicit knowledge collected by linguists for the German language. A web application and user interface were created for the algorithm, allowing the user to select different options for text decomposition, input text manually or by using a .txt file. Additionally, this project includes a script for testing the accuracy of the algorithm that was also created. The algorithm was tested on a set of words provided by the linguistic expert to measure its accuracy. The script measures both complete and partial accuracy, and a better result for accuracy measurement is achieved by testing partial accuracy, resulting in 9% better than measuring complete accuracy (87%). It can be concluded that achieving 100% accuracy is difficult, even though all the rules are implemented in the algorithm. The reason for this is that the used module does not decompose German compounds well enough. To potentially solve this problem, the model needs to be trained on the compounds found in the test set, to use another module or create exceptions manually.

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
