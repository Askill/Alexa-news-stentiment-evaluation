import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import random
import yaml

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    return question("This will take about 5 minutes. Are you Ready?")


def get_workoutplan():
    with open("workouts.yaml", 'r') as stream:
        exercises = yaml.load(stream)
    exercise_names = random.sample(list(exercises), 5)
    workout_plan = []
    for exercise_name in exercise_names:
        exercise = str(exercises[exercise_name]["duration"][0]) + " " + str(exercises[exercise_name]["duration"][1] )+ " of " + exercise_name 
        workout_plan.append(exercise)
    return workout_plan


@ask.intent('YesIntent')
def start_workout():
    workout_plan = get_workoutplan()
    response = ""
    for excercise in workout_plan[:-1]:
        response += excercise + ", "
    response += " and " + workout_plan[-1]
    return statement(workout_plan)

@ask.intent('NoIntent')
def no():
    return statement("Allright, maybe later.")

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'If you want a quick workout just say "workout"'
    return statement(speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
