import logging
import os
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import random
import yaml

def read_exercises():
    with open("workouts.yaml", 'r') as stream:
        exercises = yaml.load(stream)
    exercise_names = random.sample(list(exercises), 5)
    workout_plan = []
    for exercise_name in exercise_names:
        exercise = str(exercises[exercise_name]["duration"][0]) + " " + str(exercises[exercise_name]["duration"][1] )+ " of " + exercise_name 
        workout_plan.append(exercise)
        print(exercise)




read_exercises()