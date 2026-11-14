# (LUL/HCI/Y2T) The Kitchen that Understands: Cooking with an AI that Sees
## project basics
the project revolves on producing an application for day to day use for making a better cooking experience for the end user

Research question: Can a cooking companion that recognizes ingredients and follows the cooking progress guide a
beginner better than a recipe on a screen, and how should it speak so as not to take over the cook’s attention?

This application functions:
1) Take a photo of the ingredient the user has and propose some dish recipes based on the ingredient the user has.
2) Open the recipe and display a simple recipe step by step guide.
3) Finger out when the cooking companion should say something that will help or hinder you while cooking.
4) An app (probably cross platform) or webpage.

## to launch code
there are 2 diffrent ways

1) automatic way
* open the terminal in where the Makefile is at (where also main.py is at) and run ```make setup```
* then run either ```streamlit run main.py``` or ```make run```, dose not matter, they both do the same thing
* ```make all``` will run both ```make setup``` and ```make run```

2) manual way
* go create a vert environment ```python3 -m venv venv``` and activate it
    * linux and mac: ```source .venv/bin/activate```
    * Windows: ```source .\.venv\Scripts\activate.bat```
* install the packages needed to run the program```pip install -r requirements.txt```
* run the command ```streamlit run main.py```

if you have new packages you added, run this command ```pip freeze > requirements.txt```

you will know if the code ran by at the current stage, there is a flash of a loading screen, and then just a blank window
